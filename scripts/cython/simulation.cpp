#include "simulation.hpp"
using namespace std;
int get_rank()
{
  int rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  return rank;
}

int get_comm_size()
{
  int numtasks;
  MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
  return numtasks;
}

/*
cette version ne permet pas d'appliquer les fonctions définies dans le fichier funtions.py.
l'écoulement du flot se fait de la manière suivante:
noeud racine: distribuer son flot sur ses arrètes sortantes.
noeud intern: récupérer le flot qui est sur ses arrètes entrantes, le distribuer ensuite sur ses arrètes sortantes.
noeud feuille: récupérer le flot qui est sur ses arretes entrantes.
*/

/**
La fonction prend en paramètre un objet process, qui contient toutes les données nécessaires,
pour le calcul et la communication entre processus.
*/
void parallele_simulation(Process *process)
{
  int pid,nprocs;
  MPI_Comm_rank(MPI_COMM_WORLD,&pid);
  MPI_Comm_size(MPI_COMM_WORLD,&nprocs);
  MPI_Request request_send;
  MPI_Status status;
  //nombre de neouds qui attendent de recevoir du flot.
  int nb_noeuds_reception = 0;
  for(int i=0; i<process->getLengthNodesExterns(); i++){
    ExternNode extern_node = process->getExternNode(i);
    if(process->isToRecive(extern_node.node)){
      nb_noeuds_reception += 1;
    }
  }
  //nous permettra de recevoir, les données envoyés par les autres processus.
  int tab_reception[nb_noeuds_reception * 2];
  //autant de requette que nb_noeuds_receptionq
  MPI_Request request[nb_noeuds_reception];

  /*
  * on commence par un MPI_Isend: pour recevoir les flots envoyées par les autres processus.
  * vu qu'on peut pas attendre la reception du flot, les tests de fin de communications sont effectuer aprés les calculs.
  * de cette facon:
  * dans le premier appelle a la fonction simulation les données des neouds extern sont tout simplement initialisé a 0.
  * la mise a jour ne commence qu'a partir du deuxième appelle a la fonction 'simulation'.
  */
  for(int i=0; i<process->getLengthNodesExterns(); i++){
    ExternNode extern_node = process->getExternNode(i);
    if(process->isToRecive(extern_node.node)){
      MPI_Irecv(tab_reception+(i*2),2,MPI_INT,extern_node.num_process,32,MPI_COMM_WORLD,&request[i]);
    }
  }

  /*
  *Étape1: Noeuds Racines -> distribuer leurs flot.
  */

  /*******TRAITEMENT NODES RACINES **********/
  for (int i=0; i < process->getLengthRacines(); i++){
    int node_racine = process->getNodeRacine(i);
    int start = process->getCdegPlusNode(node_racine);
    int end = process->getCdegPlusNode(node_racine+1);
    //distribuer équitablement le flot de chaque noeud sur les arrètes sortantes.
    int flot_node = process->getFlotNode(node_racine);
    int nb_arretes_saturees = 0;
    while(flot_node > 0 && nb_arretes_saturees < (end-start)){
      int flot = flot_node/(end-start);
      for (int j=start; j<end; j++){
        int edge = process->getNplusNode(j);
        int flot_edge = process->getFlotEdge(edge);
        int capacity_edge = process->getCapacityEdge(edge);
        if((flot + flot_edge) < capacity_edge){
          process->setFlotEdges(edge,flot+flot_edge);
        }else{
          process->setFlotEdges(edge,capacity_edge);
          flot = flot - (capacity_edge - flot_edge);
          nb_arretes_saturees+=1;
        }
        flot_node -= flot;
      }
    }
    process->setFlotNode(node_racine,flot_node);
  }
  /****FIN TRAITEMENT NODE RACINES****/
  

  /*****TRAITEMENT DES NOEUDS INTERNS*****/
  for(int i=0; i<process->getLengthInsideNodes(); i++){
    int node_intern = process->getInsideNode(i);
    // a refaire: déja définie dans le tableau c_deg_moins !!
    vector<int> arretes_entrantes = process->getListEdgesIn(node_intern);
    //commencer par traiter les arretes entrantes du noeud node_intern.
    int flot_in = 0;
    //première étapes : recupérer le flot sur les arrEtes entrantes.
    for (int j=0; j < arretes_entrantes.size(); j++){
      flot_in += process->getFlotEdge(arretes_entrantes[j]);
    }
    //deuxième étape distribuer équitablement le flot sur les arretes sortantes;
    int nb_arretes_saturees = 0;
    int start = process->getCdegPlusNode(node_intern);
    int end = process-> getCdegPlusNode(node_intern+1);
    while(flot_in > 0 && nb_arretes_saturees < (end-start)){
      int flot = flot_in/(end-start);
      for (int j=start; j<end; j++){
        int edge = process->getNplusNode(j);
        int flot_edge = process->getFlotEdge(edge);
        int capacity_edge = process->getCapacityEdge(edge);
        if((flot + flot_edge) < capacity_edge){
          process->setFlotEdges(edge,flot+flot_edge);
        }else{
          process->setFlotEdges(edge,capacity_edge);
          flot = flot - (capacity_edge - flot_edge);
          nb_arretes_saturees+=1;
        }
        flot_in -= flot;
      }
    }
    process->setFlotNode(node_intern,flot_in);
  }
  
  /****FIN TRAITEMENT NODE INTERNE****/


  /********TRAITEMENT FEUILLE ******/
  for (int i=0;i<process->getLengthFeuilles();i++){
    int noeud_feuille = process->getNodeFeuille(i);
    std::vector<int> edges_in = process->getListEdgesIn(noeud_feuille);
    int flot_feuille = 0;
    for(int j=0; j<edges_in.size(); j++){
      flot_feuille += process->getFlotEdge(edges_in[j]);
    }
  }
  /*******FIN TRAITEMENT NOEUD FEUILLE*****/

  //MPI_Send: envoyé le flot des noeuds externs.

  /*********DEBUT ENVOIE*******/
  for(int i=0; i<process->getLengthInsideNodes(); i++){
    ExternNode extern_node = process->getExternNode(i);
    if(process->isToSend(extern_node.node)){
      int flot_capacity[2];
      //On send un tableau de deux élements constitué du (noeud, son flot).
      flot_capacity[0] = extern_node.node;
      flot_capacity[1] = process->getFlotNode(extern_node.node);
      MPI_Isend(flot_capacity,2,MPI_INT,extern_node.num_process,32,MPI_COMM_WORLD,&request_send);
    }
  }
  /********FIN ENVOIE********/

  // Synchronisation des communications, uniquement les requettes de reception.
  /****************DEBUT SYNCHRONISATION*******************/
  int flag;
  for (int i=0; i<nb_noeuds_reception; i++){
    MPI_Test(&request[i], &flag, &status);
    while (!flag)
    {
      MPI_Test(&request[i], &flag, &status);
    }
    int node = tab_reception[2*i];
    int flot = tab_reception[2*i+1];
    cout << "reception" << endl;
    process->setFlotNode(node,flot);
  }

  /**************************FIN*********************/
  cout << "fin du calcul" << endl;
}