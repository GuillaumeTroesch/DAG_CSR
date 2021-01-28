# Commande :
# mpiexec -n 4 python testPara.py

from mpi4py import MPI
from CSR import *
from readFile import *
from fonctions import *
from repartition import *
# from scripts.CSR import *
# from scripts.readFile import *
# from scripts.fonctions import *
# from scripts.repartition import *

# Retourne un csr a l'instant t a partir d'un csr a l'instant t-1
def simulationParallele(csr, localMap, tabCumulatifNoeud, tabCumulatifAretes, temps_max, fctRacines, fctFeuilles, fctNoeuds, fctAretes):

	### Initalisation des requetes d'envoi et de reception ###
	# e : entree, s : sortie
	req_e_noeud = {}
	req_e_arete = {}
	req_s_noeud = {}
	req_s_arete = {}

	# Buffer des noeuds et aretes a recevoir
	bufNoeuds = []
	bufAretes = []

	# Initialisation des index limites des types de noeud
	indexLocauxInternes = tabCumulatifNoeud[0]
	indexLocauxExternes = tabCumulatifNoeud[1]
	indexFeuilles = tabCumulatifNoeud[2]
	indexRacines = tabCumulatifNoeud[3]
	indexExternes = tabCumulatifNoeud[4]

	# Initialisation des index limites des types d'arete
	indexAretesInternes = tabCumulatifAretes[0]
	indexAretesExternes = tabCumulatifAretes[1]

	# Redefinition du format d'envoi et de reception avec 8 tableaux de communications extraits a partir de localMap
	# Ces tableaux definissent pour 4 d'entre eux le nombre d'elements (aretes/noeuds) a envoyer/recevoir
	# Les 4 autres tableaux contiennent les index des elements
	# De base localMap contient toutes ces informations, elles sont retraitees pour faciliter le parallelisme
	nNoeudAEnvoyer  = [0]*nb_proc
	nNoeudARecevoir = [0]*nb_proc
	nAreteAEnvoyer = [0]*nb_proc
	nAreteARecevoir = [0]*nb_proc

	indexNoeudsAEnvoyer = [None]*nb_proc
	indexNoeudsARecevoir = [None]*nb_proc
	indexAretesAEnvoyer = [None]*nb_proc
	indexAretesARecevoir = [None]*nb_proc

	( _, dictAretesARecevoir, dictAretesAEnvoyer, _, dictNoeudsARecevoir, dictNoeudsAEnvoyer) = localMap

	for n_p in range(0, nb_proc):
		if n_p in dictNoeudsAEnvoyer:
			nNoeudAEnvoyer[n_p] = len(dictNoeudsAEnvoyer[n_p])
			indexNoeudsAEnvoyer[n_p] = dictNoeudsAEnvoyer[n_p]
		if n_p in dictNoeudsARecevoir:
			nNoeudARecevoir[n_p] = len(dictNoeudsARecevoir[n_p])
			indexNoeudsARecevoir[n_p] = dictNoeudsARecevoir[n_p]
		if n_p in dictAretesAEnvoyer:
			nAreteAEnvoyer[n_p] = len(dictAretesAEnvoyer[n_p])
			indexAretesAEnvoyer[n_p] = dictAretesAEnvoyer[n_p]
		if n_p in dictAretesARecevoir:
			nAreteARecevoir[n_p] = len(dictAretesARecevoir[n_p])
			indexAretesARecevoir[n_p] = dictAretesARecevoir[n_p]
	###

	##### Boucle de la simulation (chaque iteration represente une simulation du dag a l'instant t) #####
	for temps in range(1, temps_max+1):

		# Nouvelles valeurs des noeuds
		valeurNoeuds2 = [None] * len(csr.getValeurNoeuds())
		valeurAretes2 = []

		### traitement des noeuds locaux internes ###
		for idNoeud in range(0, indexLocauxInternes):
			(flot, capacite) = csr.getValeurNoeud(idNoeud)
			new_flot1 = fctNoeuds(temps, idNoeud, csr)
			valeurNoeuds2[idNoeud] = (new_flot1, capacite)
		###

		### Envoi des noeuds traites aux processeurs dependants ###
		for rank_p in range(0, nb_proc):
			l_tupleNoeud = []
			if not rank_p == rank and not nNoeudAEnvoyer[rank_p] == 0 :
				for i in range(0, nNoeudAEnvoyer[rank_p]):
					valeurNoeud = csr.getValeurNoeudByName(indexNoeudsAEnvoyer[rank_p][i])
					l_tupleNoeud.append([indexNoeudsAEnvoyer[rank_p][i], valeurNoeud])

				req_s_noeud[rank_p] = comm.isend(l_tupleNoeud, dest=rank_p, tag=500+rank_p)
		###

		### Envoi des aretes traites aux processeurs dependants ###
		for rank_p in range(0, nb_proc):
			l_tupleArete = []
			if not rank_p == rank and not nAreteAEnvoyer[rank_p] == 0:
				for i in range(0, nAreteAEnvoyer[rank_p]):
					valeurArete = csr.getValeurAreteByName(indexAretesAEnvoyer[rank_p][i])
					l_tupleArete.append([indexAretesAEnvoyer[rank_p][i], valeurArete])

				req_s_arete[rank_p] = comm.isend(l_tupleArete, dest=rank_p, tag=600 + rank_p)
		###

		### Recuperation des noeuds dont depend le processeur ###
		for rank_p in range(0, nb_proc):
			if not rank_p == rank and not nNoeudARecevoir[rank_p] == 0:
				req_e_noeud[rank_p] = comm.irecv(source = rank_p, tag=500 + rank)
		###

		### Recuperation des aretes dont depend le processeur ###
		for rank_p in range(0, nb_proc):
			if not rank_p == rank and not nAreteARecevoir[rank_p] == 0:
				req_e_arete[rank_p] = comm.irecv(source=rank_p, tag=600 + rank)
		###

		### blocage en attente de reception ###
		for rank_p in range(0, nb_proc):
			if not rank_p == rank:
				if not nNoeudARecevoir[rank_p] == 0:
					bufNoeuds += req_e_noeud[rank_p].wait()
				if not nAreteARecevoir[rank_p] == 0:
					bufAretes += req_e_arete[rank_p].wait()
				if not nNoeudAEnvoyer[rank_p] == 0:
					req_s_noeud[rank_p].wait()
				if not nAreteAEnvoyer[rank_p] == 0:
					req_s_arete[rank_p].wait()
		###

		#Set sur les valeurs des noeuds et des aretes recuperees des autres processeurs
		for noeud in bufNoeuds:
			numNoeud = noeud[0]
			valeurNoeud = noeud[1]
			csr.setValeurNoeud(csr.getNumNoeud(numNoeud), valeurNoeud)

		for arete in bufAretes:
			numArete = arete[0]
			valeurArete = arete[1]
			csr.setValeurArete(csr.getIndexAreteByName(numArete), valeurArete)


		##### Traitement des donnees dependantes #####
		### traitement des noeuds locaux externes ###
		for idNoeud in range(indexLocauxInternes, indexLocauxExternes):
			(flot, capacite) = csr.getValeurNoeud(idNoeud)
			# fctNoeud
			new_flot1 = fctNoeuds(temps, idNoeud, csr)
			valeurNoeuds2[idNoeud] = (new_flot1, capacite)
		###

		### Traitement des feuilles ###
		for idNoeud in range(indexLocauxExternes, indexFeuilles):
			(flot, capacite) = csr.getValeurNoeud(idNoeud)
			# fctNoeud
			new_flot1 = fctNoeuds(temps, idNoeud, csr)
			# fctFeuille
			new_flot2 = fctFeuilles(temps, idNoeud, flot)
			valeurNoeuds2[idNoeud] = (min(max(new_flot1 - new_flot2, 0), capacite), capacite)
		###

		### Traitement des racines ###
		for idNoeud in range(indexFeuilles, indexRacines):
			(flot, capacite) = csr.getValeurNoeud(idNoeud)
			# fctNoeud
			new_flot1 = fctNoeuds(temps, idNoeud, csr)
			# fctRacine
			new_flot2 = fctRacines(temps, idNoeud)
			valeurNoeuds2[idNoeud] = (min(new_flot1 + new_flot2, capacite), capacite)
		###

		### Traitement des aretes ###
		for idArete in range(0, indexAretesInternes):
			# fctArete
			new_flot = fctArete(temps, idArete, csr)
			valeurAretes2.append((new_flot, csr.getValeurArete(idArete)[1]))

		for idArete in range(indexAretesInternes, indexAretesExternes):
			valeurAretes2.append(None)

		### Setter du graphe t ###
		csr.setValeursNoeuds(valeurNoeuds2)
		csr.setValeursAretes(valeurAretes2)

	return csr


# Debut de la parallelisation
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nb_proc = comm.size
rank_proc_root = 0

localCsr = None
localMap = None

globalCsr = None

fctRacines = flotRacine5
fctFeuilles = ecoulementFeuille4
fctNoeuds = fctNoeuds1
fctArete = fctArete1

tabCumulatifNoeud = []
tabCumulatifArete = []
globalCsr = []
temps_max = 8

if rank == rank_proc_root:
	globalCsr = readFileDot("../examples/DAG5.dot", "../examples/DAG5_val_edges.pmap", "../examples/DAG5_val_nodes.pmap")

	globalCsr.appliquerFctRacine(fctRacines, 0)
	globalCsr.afficher()
	print()
	reparti = repartition(globalCsr, 4)
	map = mapsDesEchanges(reparti)
	localsRepartitionOrdonnee = setRepartitionOrdonnee(reparti, globalCsr)
	localsCsr = reconstituerCsr(localsRepartitionOrdonnee[0],localsRepartitionOrdonnee[1], globalCsr, localsRepartitionOrdonnee[2])

### Distribution des tableaux et du mini-csr aux processeurs associes ###
	localCsr = localsCsr[rank_proc_root]
	localMap = map[rank_proc_root]
	tabCumulatifNoeud = localsRepartitionOrdonnee[2][rank_proc_root]
	tabCumulatifArete = localsRepartitionOrdonnee[3][rank_proc_root]

	for i in range(1, nb_proc):
		comm.send(localsCsr[i], dest=i, tag=10 + i)
		comm.send(map[i], dest=i, tag=100 + i)
		comm.send(localsRepartitionOrdonnee[2][i], dest=i, tag=200 + i)
		comm.send(localsRepartitionOrdonnee[3][i], dest=i, tag=300 + i)
else:
	localCsr = comm.recv(source=rank_proc_root, tag=10 + rank)
	localMap = comm.recv(source=rank_proc_root, tag=100 + rank)
	tabCumulatifNoeud = comm.recv(source=rank_proc_root, tag=200 + rank)
	tabCumulatifArete = comm.recv(source=rank_proc_root, tag=300 + rank)
###


csrLocalFinal = simulationParallele(localCsr, localMap, tabCumulatifNoeud, tabCumulatifArete, temps_max, fctRacines, fctFeuilles, fctNoeuds, fctArete)

### Reconstitution du CSR global ###
# Recuperation des csr_locaux
listeCsr = []
if rank == rank_proc_root:
	listeCsr = [csrLocalFinal]
	for i in range(1, nb_proc):
		listeCsr.append(comm.recv(source=i, tag=700 + i))
else:
	comm.send(csrLocalFinal, dest=rank_proc_root, tag=700 + rank)

# Reconstitution du Csr global
if rank == rank_proc_root:
	valeurnoeuds = [None] * globalCsr.getNbNoeuds()
	for i in range(globalCsr.getNbNoeuds()):
		val = None
		for miniCsr in listeCsr:
			tmp = miniCsr.getValeurNoeudByName(i)
			if (tmp != -1 and tmp != None):
				val = tmp
				break
		valeurnoeuds[i] = val
	globalCsr.setValeursNoeuds(valeurnoeuds)

	valeurAretes = [None] * globalCsr.getNbAretes()
	for i in range(globalCsr.getNbAretes()):
		val = None
		for miniCsr in listeCsr:
			tmp = miniCsr.getValeurAreteByName(i)
			if (tmp != -1 and tmp != None):
				val = tmp
				break
		valeurAretes[i] = val
	globalCsr.setValeursAretes(valeurAretes)

	globalCsr.afficher()
	# exportFileDot(globalCsr, "./testExportCSR.dot")
