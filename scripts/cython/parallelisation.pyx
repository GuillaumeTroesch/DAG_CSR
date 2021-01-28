from cpython cimport array
#pour les allocations mémoire.
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
import array
from libcpp.vector cimport vector

#on cython les structures sont définies comme des class.
cdef extern from "process.hpp":
	cdef cppclass ExternNode:
		int node
		int num_process

cdef extern from "process.hpp":
	cdef cppclass FlotCapacity:
		int flot
		int capacity

#redéfinition de la classe et de ses méthodes, pour pouvoir les invoquées.
cdef extern from "process.hpp":
	cdef cppclass Process:
		Process();
		Process(int *c_plus, int *c_moins, int *n_plus, int *n_moins, int *sources, int *destinations)
		int getCdegPlusNode(int node)const
		int getCdegMoinsNode(int node) const
		int getNplusNode(int position) const
		int getNmoinsNode(int position) const
		int getSourceEdge(int edge) const
		int getDestinationEdge(int edge) const
		int getNodeRacine(int position) const
		int getNodeFeuille(int position) const
		void addExternNode(int node, int num_process)
		ExternNode getExternNode(int position) const
		int getInsideNode(int position)const
		int isToSend(int n) const
		int isToRecive(int n) const
		void setNodesFeuilles(int *feuilles)
		void setNodesRacines(int *racines)
		void setInsideNodes(int *noeuds)
		void addNodeFlotapacity(int flot,int capacity)
		void addEdgesFlotCapacity(int flot,int capacity)
		#en cython vector ce declare de la manière ci-dessous a la place de vector<int>
		vector[int] getListEdgesIn(int node) const
	   	#setters:
		void setLengthNodes(int length)
		void setLengthEdges(int length)
		void setLengthCdegPlus(int length)
		void setLengthCdegMoins(int length)
		void setLengthNplus(int length)
		void setLengthNmoins(int length)
		void setLengthSourcesAndDestinations(int length)
		void setLengthRacines(int length)
		void setLengthFeuilles(int length)
		void setLengthInsideNodes(int length)
		void setFlotNode(int node, int flot_node)
		void setFlotEdges(int edge, int flot_edge)

	    #getters.
		int getLengthNodes()const
		int getLengthEdges()const
		int getLengthCdegPlus()const
		int getLengthCdegMoins()const
		int getLengthNplus()const
		int getLengthNmoins()const
		int getLengthSources()const
		int getLengthDestinations()const
		int getLengthRacines()const
		int getLengthFeuilles()const
		int getLengthInsideNodes()const
		int getLengthNodesExterns()const
		int getFlotNode(int node)const
		int getCapacityNode(int node)const
		int getFlotEdge(int edge)const
		int getCapacityEdge(int edge)const
		
cdef extern from "simulation.hpp":
	cpdef int get_rank()
	cpdef int get_comm_size()
	cdef void parallele_simulation(Process *process)


"""
la fonction recevera en paramètre.
1-cdegPlus: degré cumulé d'un sommet, qui nous permetra de récupérer les indices de ses arretes sortantes.
2-cdegMoins : degré cumulé d'un sommet, qui nous permetra de récupérer les indices de ses arretes entrantes.
3-nPlus : définie l'enssemble des arrètes sortantes d'un noued.
4-nMoins : défnie l'enssemble des arrétes entrantes d'un noeud.
5-sources: définie pour chaque arrète son noeud source.
6-destination: définie pour chaque arrète son noued destiniation.
en plus des 6 tableaux:
7-un septième tabealu qui définie les noeuds externes au processus de la sorte [('nom ou indice du noeud',numProcessus)....]:
pour facilliter la gestion des communication.
8-vecteur des noeuds feuilles,vecteur des noeuds racines ainsi que le vecteur des noeuds interns.
"""
def simulation_parallele():
	#Notes:
	"""
	#cython ne gère pas la conversion automatique des objets python en des pointeurs c++ ou c.
	#pour convertir un tableau python en tableau c++:
	---->cdef int *cpp_array = <int*>PyMem_Malloc(len(python_array) * sizeof(int)).
	#pour désallouer la mémoire allouée:
	---->PyMem_Free(cpp_array).
	pour rendre une fonction sollicitable depuis un code python 'file.py' il faudra prédéder la déclaration de la fonction d'un cpdef.
	"""
	

	"""
	difficultées rencontrées:
	cette fonction n'a pas été complété, car nous n'avons pas trouvé la facon de convertir une fonction python en une fonction c++.
	du fait que les fonctions fournit par l'utilisateur sont écrites en python (c'est pour cette raison nous n'avons pas envisagé de récrire les fonctions en c++)
	et donc la meilleure solution serait de trouver un moyen qui nous permettra de convertir les fonctions python, vers des fonctions c++.
	"""
	return 0