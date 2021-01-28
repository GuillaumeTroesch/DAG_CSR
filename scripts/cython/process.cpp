#include "process.hpp"
#include <iostream>
using namespace std;

Process::Process(int *c_plus, int *c_moins, int *n_plus, int *n_moins, int *sources, int *destinations){
    m_cdeg_plus  = c_plus ;
    m_cdeg_moins = c_moins;
    m_n_plus = n_plus;
    m_n_moins = n_moins;
    m_sources = sources;
    m_destinations = destinations;
}

int Process::getCdegPlusNode(int node) const{
    return m_cdeg_plus[node];
}

int Process::getCdegMoinsNode(int node) const{
    return m_cdeg_moins[node];
}

int Process::getNplusNode(int position) const{
    return m_n_plus[position];
}

int Process::getNmoinsNode(int position) const{
    return m_n_moins[position];
}

int Process::getSourceEdge(int edge) const{
    return m_sources[edge];
}

int Process::getDestinationEdge(int edge) const{
    return m_destinations[edge];
}

int Process::getNodeRacine(int position) const{
    return m_racines[position];
}

int Process::getInsideNode(int position) const{
    return m_inside_nodes[position];
}
int Process::getNodeFeuille(int position) const{
    return m_feuilles[position];
}


void Process::addNodeFlotapacity(int flot,int capacity){
    FlotCapacity *flot_capcity = (FlotCapacity *)malloc(sizeof(FlotCapacity));
    flot_capcity->flot = flot;
    flot_capcity->capacity = capacity;
    m_nodes_flot_capacity.push_back(flot_capcity);
}

void Process::addEdgesFlotCapacity(int flot,int capacity){
    FlotCapacity *flot_capcity = (FlotCapacity *)malloc(sizeof(FlotCapacity));
    flot_capcity->flot = flot;
    flot_capcity->capacity = capacity;
    m_edges_flot_capacity.push_back(flot_capcity);
}
//renvoie la liste des arretes(position de l'arretes) entrantes du noeud node. 
//un noeud n possède des arretes entrantes, s'il appartient au tableau mèdestination.
std::vector<int> Process::getListEdgesIn(int node) const{
    vector <int> list_edges;
    for(int i=0; i<getLengthDestinations();i++){
        if(m_destinations[i] == node){
            list_edges.push_back(i);
        }
    }
    return list_edges;
}    

ExternNode Process::getExternNode(int position) const{
    return nodes_externs[position];
}

void Process::addExternNode(int node, int num_process){
    ExternNode node_extern;
    node_extern.node = node;
    node_extern.num_process = num_process;
    nodes_externs.push_back(node_extern);
}

int Process::getLengthNodesExterns()const{
    return nodes_externs.size();
}
//setters.
void Process::setLengthEdges(int length){
    length_edges = length;
}

void Process::setLengthCdegPlus(int length){
    length_cdeg_plus = length;
}

void Process::setLengthCdegMoins(int length){
    length_cdeg_moins = length;
}

void Process::setLengthNplus(int length){
    length_n_plus = length;
}

void Process::setLengthNmoins(int length){
    length_n_moins = length;
}

void Process::setLengthSourcesAndDestinations(int length){
    length_sources_and_destinations = length;
}

void Process::setLengthRacines(int length){
    length_racines = length;
}

void Process::setLengthFeuilles(int length){
    length_feuilles = length;
}

void Process::setLengthInsideNodes(int length){
    length_inside_nodes = length;
}

void Process::setFlotNode(int node, int flot_node){
    m_nodes_flot_capacity[node]->flot = flot_node;
}

void Process::setFlotEdges(int edge, int flot_edge){
    m_edges_flot_capacity[edge]->flot = flot_edge;
}

    //getters.
int Process::getLengthNodes() const{
    return length_nodes;
}

int Process::getLengthEdges() const{
    return length_edges;
}

int Process::getLengthCdegPlus() const{
    return length_cdeg_plus;
}

int Process::getLengthCdegMoins() const{
    return length_cdeg_moins;
}

int Process::getLengthNplus() const{
    return length_n_plus;
}

int Process::getLengthNmoins() const{
    return length_n_moins;
}

int Process::getLengthSources() const{
    return length_sources_and_destinations;
}

int Process::getLengthDestinations() const{
    return length_sources_and_destinations;
}

int Process::getLengthRacines() const{
    return length_racines;
}

int Process::getLengthFeuilles() const{
    return length_feuilles;
}

int Process::getLengthInsideNodes() const{
    return length_inside_nodes;
}

int Process::getFlotNode(int node) const{
    return m_nodes_flot_capacity[node]->flot;
}

int Process::getCapacityNode(int node) const{
    m_nodes_flot_capacity[node]->capacity;
}

int Process::getFlotEdge(int edge) const{
    return m_edges_flot_capacity[edge]->flot;
}

int Process::getCapacityEdge(int edge) const{
    return m_edges_flot_capacity[edge]->capacity;
}

/****/
//ces deux fonctions nous permettent de savoir si on doit envoyer ou recevoir le flot d'un noeud.
int Process::isToSend(int node) const{
    for(int i=0; i<getLengthSources(); i++){
        if(m_sources[i] == node){
            return 1;
        }
    }
    return 0;
}

int Process::isToRecive(int node) const{
    for(int i=0; i<getLengthDestinations(); i++){
        if(m_destinations[i] == node){
            return 1;
        }
    }
    return 0;
}
/*****/

void Process::setNodesFeuilles(int *feuilles){
    m_feuilles = feuilles;
}

void Process::setNodesRacines(int *racines){
    m_racines = racines;
}

void Process::setInsideNodes(int *noeuds){
    m_inside_nodes = noeuds;
}



Process::~Process(){}
