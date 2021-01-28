#ifndef PAR_PROCESS
#define PAR_PROCESS
#include <vector>


//liste des noeuds extern pour un processus
//un noeud extern est définie par sa valeur et le numéro du processus auquel il appartient.
typedef struct ExternNode
{
    int node;
    int num_process;
}ExternNode;

//stocker le flot et la capacité d'un noeud ou d'une arrète.
typedef struct FlotCapacity
{
	int flot;
	int capacity;
}FlotCapacity;

class Process
{
    public:
    Process();
    Process(int *c_plus, int *c_moins, int *n_plus, int *n_moins, int *sources, int *destinations);
    //les 6 tableaux, comme définie dans la thèse de Hélène coulon.
    int getCdegPlusNode(int node)const;
    int getCdegMoinsNode(int node) const;
    int getNplusNode(int position) const;
    int getNmoinsNode(int position) const;
    int getSourceEdge(int edge) const;
    int getDestinationEdge(int edge) const;
    int getNodeRacine(int position) const;

    
    int getNodeFeuille(int position) const;
    void addExternNode(int node, int num_process);
    ExternNode getExternNode(int position) const;
    //partir sur le principe qu'un noeud intern ne peut pas etre un oeud extern d'un processus.
    int getInsideNode(int position)const;
    //pour savoir si un on doit envoyer ou recevoir le flot d'un noeud.
    int isToSend(int n) const;
    int isToRecive(int n) const;
    //noeuds racines, noeuds feuilles et noueds internes.
    void setNodesFeuilles(int *feuilles);
    void setNodesRacines(int *racines);
    void setInsideNodes(int *noeuds);
    //ajouter un noeud avec son flot et sa capacité a la liste des neouds.
    void addNodeFlotapacity(int flot,int capacity);
    //ajouter un arrete avec son flot et sa capacité a la liste des neouds.
    void addEdgesFlotCapacity(int flot,int capacity);
    //renvoie la liste des arretes(position de l'arretes) entrantes du noeud node. 
    //un noeud n possède des arretes entrantes, si n appartient au tableau m_destination.
    std::vector<int> getListEdgesIn(int node) const;
    
    //setters.
    void setLengthNodes(int length);
    void setLengthEdges(int length);
    void setLengthCdegPlus(int length);
    void setLengthCdegMoins(int length);
    void setLengthNplus(int length);
    void setLengthNmoins(int length);
    void setLengthSourcesAndDestinations(int length);
    void setLengthRacines(int length);
    void setLengthFeuilles(int length);
    void setLengthInsideNodes(int length);
    void setFlotNode(int node, int flot_node);
    void setFlotEdges(int edge, int flot_edge);

    //getters.
    int getLengthNodes()const;
    int getLengthEdges()const;
    int getLengthCdegPlus()const;
    int getLengthCdegMoins()const;
    int getLengthNplus()const;
    int getLengthNmoins()const;
    int getLengthSources()const;
    int getLengthDestinations() const;
    int getLengthRacines() const;
    int getLengthFeuilles() const;
    int getLengthInsideNodes() const;
    int getLengthNodesExterns()const;
    int getFlotNode(int node)const;
    int getCapacityNode(int node)const;
    int getFlotEdge(int edge)const;
    int getCapacityEdge(int edge)const;
 	~Process();
    private:

    int length_nodes;
    int length_edges;
    int length_cdeg_plus;
    int length_cdeg_moins;
    int length_n_plus;
    int length_n_moins;
    int length_sources_and_destinations;
    int length_racines;
    int length_feuilles;
    int length_inside_nodes;
    int length_nodes_externs;
    //flot et capacité des noeuds et des arrètes.
 	std::vector<FlotCapacity*> m_nodes_flot_capacity;
 	std::vector<FlotCapacity*> m_edges_flot_capacity;
    //noeuds externs.
    std::vector<ExternNode> nodes_externs;
    
    int *m_cdeg_plus;
    int *m_cdeg_moins;
    int *m_n_plus;
    int *m_n_moins;
    int *m_sources;
    int *m_destinations;

    //feuilles, racines, noeuds internes.
    int *m_feuilles;
    int *m_racines;
    int *m_inside_nodes;

    
    

};
 
#endif