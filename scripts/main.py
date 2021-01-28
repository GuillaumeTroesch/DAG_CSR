from CSR import *
from readFile import *
from fonctions import *


# Retourne un csr a l'instant t a partir d'un csr a l'instant t-1
def simulation(csr, temps, fctRacines, fctFeuilles, fctNoeuds, fctAretes):
	valeurNoeuds2 = [None]*len(csr.getValeurNoeuds())
	valeurAretes2 = []
	
	#Racines
	for idNoeud in csr.getNoeudsRacines():
		(flot, capacite) = csr.getValeurNoeud(idNoeud)
		#fctNoeud
		new_flot1 = fctNoeuds(temps, idNoeud, csr)
		#fctRacine
		new_flot2 = fctRacines(temps, idNoeud)
		
		valeurNoeuds2[idNoeud] = (min(new_flot1+new_flot2, capacite), capacite)
	
	#Internes
	for idNoeud in csr.getNoeudsInternes(): 
		(flot, capacite) = csr.getValeurNoeud(idNoeud)
		#fctNoeud
		new_flot1 = fctNoeuds(temps, idNoeud, csr)
		
		valeurNoeuds2[idNoeud] = (new_flot1, capacite)
		
	#Feuilles
	for idNoeud in csr.getNoeudsFeuilles():
		(flot, capacite) = csr.getValeurNoeud(idNoeud)
		#fctNoeud
		new_flot1 = fctNoeuds(temps, idNoeud, csr)
		#fctFeuille
		new_flot2 = fctFeuilles(temps, idNoeud, flot)
		
		valeurNoeuds2[idNoeud] = (min(max(new_flot1 - new_flot2, 0), capacite), capacite)
		
	#Aretes
	for idArete in range(len(csr.getValeursAretes())):
		#fctArete
		new_flot = fctArete(temps, idArete, csr)
		
		valeurAretes2.append((new_flot, csr.getValeurArete(idArete)[1]))
		
	csr.setValeursNoeuds(valeurNoeuds2)
	csr.setValeursAretes(valeurAretes2)
				
		
fctRacines = flotRacine5
fctFeuilles = ecoulementFeuille4
fctNoeuds = fctNoeuds1
fctArete = fctArete1
	
# csr = readFileDot("../examples/DAG1.dot", "../examples/DAG1_val_edges.pmap", "../examples/DAG1_val_nodes.pmap")
csr = readFileDot("../examples/DAG5.dot", "../examples/DAG5_val_edges.pmap", "../examples/DAG5_val_nodes.pmap")
# csr = readFileDot("../examples/test2.dot", "../examples/test2_val_edges.pmap", "../examples/test2_val_nodes.pmap")
# csr = readFileDot("../examples/DAG1.dot", "../examples/DAG1_val_edges.pmap", "../examples/DAG1_val_nodes.pmap")
# csr = readFileDot("../examples/test.dot", "", "")

csr.appliquerFctRacine(fctRacines, 0)
csr.afficher()
print()
# exportFileDot(csr, "./testExportCSR.dot")

temps_max = 8 
for t in range(1, temps_max+1):
	simulation(csr, t, fctRacines, fctFeuilles, fctNoeuds, fctArete)
	csr.afficher()
	print()
	# exportFileDot(csr, "./testExportCSR.dot")

	