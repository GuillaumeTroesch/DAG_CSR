from CSR import *
from readFile import *
from fonctions import *


# Retourne un csr a l'instant t a partir d'un csr a l'instant t-1
def simulation(csr, temps, fctRacine, fctFeuille, fctDistribution, fctAccumulation):
	tmp_valeurNoeuds = csr.getValeurNoeuds()
	valeurNoeuds2 = [None]*len(tmp_valeurNoeuds)
	tmp_valeurAretes = csr.getValeurAretes()
	valeurAretes2 = [None]*len(tmp_valeurAretes)
	
	#Feuilles
	for idFeuille in csr.getNoeudsFeuilles():
		(flot, capacite) = tmp_valeurNoeuds[idFeuille]
		nomNoeud = csr.getNomNoeud(idFeuille)
		
		#fctFeuille
		#On modifie la valeur du noeud
		val = fctFeuille(temps, nomNoeud, flot)
		
		#fctAccumulation
		#On modifie la valeur du noeud et la valeur des aretes entrantes
		# set noeud
		capacite_restante = capacite-val # la capacite_restante du noeud est sa	capacite - la valeur du flot qu'on lui a deja assignee par une autre fct (par exemple par fctFeuille)
		(tmp_val, tmp_aretes) = fctAccumulation(temps, nomNoeud, capacite_restante, csr.getFlotAretesE(idFeuille))
		val += tmp_val
		listeIdAretesE = csr.getAretesEntrantesNoeuds(idFeuille)
		# set aretes entrantes
		for i in range(len(tmp_aretes)):
			if (valeurAretes2[listeIdAretesE[i]] == None):
				flot_arete = tmp_aretes[i]
			else:
				flot_arete = tmp_aretes[i] + valeurAretes2[listeIdAretesE[i]][0]
			capacite_arete = tmp_valeurAretes[listeIdAretesE[i]][1]
			valeurAretes2[listeIdAretesE[i]] = (flot_arete, capacite_arete)
		
		valeurNoeuds2[idFeuille] = (val, capacite)
		
	#Internes
	for idInterne in csr.getNoeudsInternes()[::-1]: #[::-1] equivalent a reverse #TODO en commencant par les noeuds du bas, ca marchera. Ici on est pas certain que reverse suffise : si les noeuds sont ranges dans le desordre
		(flot, capacite) = tmp_valeurNoeuds[idInterne] 
		valeurNoeuds2[idInterne] = (fctFeuille(temps, csr.getNomNoeud(idInterne), flot), capacite)
		
		#fctDistribution
		#On modifie la valeur du noeud et la valeur des aretes sortantes
		# set noeud
		(listeIdAretesS, capacitesAretesS) = csr.getAretesS(idInterne)
		for i in range(len(listeIdAretesS)): #On redefini chaque capacite comme etant la capacite restante sur une arete, c-a-d capacite - flot deja attribue par une fct precedente
			id = listeIdAretesS[i]
			capacitesAretesS[i] -= valeurAretes2[id][0]
		(tmp_val, tmp_aretes) = fctDistribution(temps, nomNoeud, flot, capacitesAretesS)
		val = tmp_val
		# set aretes sortantes
		for i in range(len(tmp_aretes)):
			if (valeurAretes2[listeIdAretesS[i]] == None):
				flot_arete = tmp_aretes[i]
			else:
				flot_arete = tmp_aretes[i] + valeurAretes2[listeIdAretesS[i]][0] 
			capacite_arete = tmp_valeurAretes[listeIdAretesS[i]][1]
			valeurAretes2[listeIdAretesS[i]] = (flot_arete, capacite_arete) 
			
		#fctAccumulation
		#On modifie la valeur du noeud et la valeur des aretes entrantes
		# set noeud
		capacite_restante = capacite-val # la capacite_restante du noeud est sa	capacite - la valeur du flot qu'on lui a deja assignee par une autre fct (par exemple par fctDistribution)
		(tmp_val, tmp_aretes) = fctAccumulation(temps, nomNoeud, capacite_restante, csr.getFlotAretesE(idInterne))
		val += tmp_val
		listeIdAretesE = csr.getAretesEntrantesNoeuds(idInterne)
		# set aretes entrantes
		for i in range(len(tmp_aretes)):
			if (valeurAretes2[listeIdAretesE[i]] == None):
				flot_arete = tmp_aretes[i]
			else:
				flot_arete = tmp_aretes[i] + valeurAretes2[listeIdAretesE[i]][0] 
			capacite_arete = tmp_valeurAretes[listeIdAretesE[i]][1]
			valeurAretes2[listeIdAretesE[i]] = (flot_arete, capacite_arete) 
			
		valeurNoeuds2[idInterne] = (val, capacite)
		
	#Racines
	for idRacine in csr.getNoeudsRacines():
		(flot, capacite) = tmp_valeurNoeuds[idRacine]
		nomNoeud = csr.getNomNoeud(idRacine)
		
		#fctDistribution
		#On modifie la valeur du noeud et la valeur des aretes sortantes
		# set noeud
		(listeIdAretesS, capacitesAretesS) = csr.getAretesS(idRacine)
		for i in range(len(listeIdAretesS)): #On redefini chaque capacite comme etant la capacite restante sur une arete, c-a-d capacite - flot deja attribue par une fct precedente
			id = listeIdAretesS[i]
			capacitesAretesS[i] -= valeurAretes2[id][0]
		(tmp_val, tmp_aretes) = fctDistribution(temps, nomNoeud, flot, capacitesAretesS)
		val = tmp_val
		# set aretes sortantes
		for i in range(len(tmp_aretes)):
			if (valeurAretes2[listeIdAretesS[i]] == None):
				flot_arete = tmp_aretes[i]
			else:
				flot_arete = tmp_aretes[i] + valeurAretes2[listeIdAretesS[i]][0] 
			capacite_arete = tmp_valeurAretes[listeIdAretesS[i]][1]
			valeurAretes2[listeIdAretesS[i]] = (flot_arete, capacite_arete)
		
		#fctRacine
		val += fctRacine(temps, nomNoeud)
		
		valeurNoeuds2[idRacine] = (val, capacite)
		
	return CSR(csr.getNoeuds(), valeurNoeuds2, csr.getIndex(), csr.getVoisins(), valeurAretes2, csr.getListParentEdge())
		
		
fctRacine = flotRacine5
fctFeuille = ecoulementFeuille4
fctDistribution = separationNoeud5
fctAccumulation = accumulationNoeud4
	
# csr = readFileDot("../examples/DAG1.dot", "../examples/DAG1_val_edges.pmap", "../examples/DAG1_val_nodes.pmap")
csr = readFileDot("../examples/DAG5.dot", "../examples/DAG5_val_edges.pmap", "../examples/DAG5_val_nodes.pmap")
# csr = readFileDot("../examples/DAG1.dot", "../examples/DAG1_val_edges.pmap", "../examples/DAG1_val_nodes.pmap")
# csr = readFileDot("../examples/test.dot", "", "")

csr.appliquerFctRacine(fctRacine, 0)
csr.afficher()
print()
# exportFileDot(csr, "./testExportCSR.dot")


csr2 = simulation(csr, 1, fctRacine, fctFeuille, fctDistribution, fctAccumulation)
csr2.afficher()
print()
# exportFileDot(csr2, "./testExportCSR2.dot")

csr3 = simulation(csr2, 2, fctRacine, fctFeuille, fctDistribution, fctAccumulation)
csr3.afficher()
print()
# exportFileDot(csr3, "./testExportCSR3.dot")

csr4 = simulation(csr3, 2, fctRacine, fctFeuille, fctDistribution, fctAccumulation)
csr4.afficher()
print()
# exportFileDot(csr4, "./testExportCSR4.dot")
	