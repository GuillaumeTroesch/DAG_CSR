from CSR import *
from readFile import *

#Retourne un resultat de la forme :
# [([aretes à traiter dans proc 0], [aretes ext de proc 0], [noeuds à traiter dans proc 0], [noeuds ext de proc 0]), (.., .., .., ..), ...]


def repartition(csr, nbProcs):
	res=[]
	repartitionNbAretesSurProcs = [csr.getNbAretes()//nbProcs]*nbProcs
	for i in range(csr.getNbAretes()%nbProcs):
		repartitionNbAretesSurProcs[i]+=1

	repartitionNbNoeudsSurProcs = [csr.getNbNoeuds()//nbProcs]*nbProcs
	for i in range(csr.getNbNoeuds()%nbProcs):
		repartitionNbNoeudsSurProcs[i]+=1

	aretesDejaChoisies = []
	aretesRestantes = csr.getNumAretes()
	noeudsDejaChoisis = []
	for numProc in range(nbProcs): #TODO range(nbProcs)
		aretesChoisies=[]
		aretesExt=[]
		#Repartir les aretes
		# Etape 1
		# Chercher un noeud qui a le plus d'arete entrantes ou sortantes, nb ne dépassant pas le nb max d'aretes dans un proc
		# en cas degalites, privilegier les feuilles ou racines
		maxi = -1
		noeudDepart = -1
		aretesEntrantesChoisies = False
		for idNoeud in csr.getNoeudsInternes():
			aretesEntrantes = csr.getAretesEntrantesNoeud(idNoeud)
			aretesSortantes = csr.getAretesSortantesNoeud(idNoeud)
			for idArete in aretesEntrantes[::-1]: #On ne prend pas les aretes deja prises par d'autres procs
				if idArete in aretesDejaChoisies:
					aretesEntrantes.remove(idArete)
			for idArete in aretesSortantes[::-1]: #On ne prend pas les aretes deja prises par d'autres procs
				if idArete in aretesDejaChoisies:
					aretesSortantes.remove(idArete)
			e = len(aretesEntrantes)
			s = len(aretesSortantes)
			if (maxi<e and e<=repartitionNbAretesSurProcs[numProc]):
				maxi = e
				noeudDepart = idNoeud
				aretesEntrantesChoisies = True
			if (maxi<s and s<=repartitionNbAretesSurProcs[numProc]):
				maxi = s
				noeudDepart = idNoeud
				aretesEntrantesChoisies = False
		for idNoeud in csr.getNoeudsFeuilles()+csr.getNoeudsRacines(): #pour les feuilles ou racines, on autorise à override un max egal
			aretesEntrantes = csr.getAretesEntrantesNoeud(idNoeud)
			aretesSortantes = csr.getAretesSortantesNoeud(idNoeud)
			for idArete in aretesEntrantes[::-1]: #On ne prend pas les aretes deja prises par d'autres procs
				if idArete in aretesDejaChoisies:
					aretesEntrantes.remove(idArete)
			for idArete in aretesSortantes[::-1]: #On ne prend pas les aretes deja prises par d'autres procs
				if idArete in aretesDejaChoisies:
					aretesSortantes.remove(idArete)
			e = len(aretesEntrantes)
			s = len(aretesSortantes)
			if (maxi<=e and e<=repartitionNbAretesSurProcs[numProc]):
				maxi = e
				noeudDepart = idNoeud
				aretesEntrantesChoisies = True
			if (maxi<=s and s<=repartitionNbAretesSurProcs[numProc]):
				maxi = s
				noeudDepart = idNoeud
				aretesEntrantesChoisies = False

		# Toutes les aretes comptées sont ajoutees au proc
		noeudsContenus=[noeudDepart]
		if (aretesEntrantesChoisies):
			idAretesChoisies = csr.getAretesEntrantesNoeud(noeudDepart)

		else:
			idAretesChoisies = csr.getAretesSortantesNoeud(noeudDepart)
		for idArete in idAretesChoisies:
			aretesRestantes.remove(idArete)



		# Etape 2
		# Compléter le proc avec des aretes paralleles, choisir en priorite :
		# 1) si aucune arete parallele, prendre le max d'aretes entrantes ou sortantes sur un noeud deja considere, en ajoutant le moins d'aretes paralleles possible
		# 2) une arete parallele qui ajoute le moins d'aretes paralleles (choisir plusieurs aretes, et comptabiliser le nb d'aretes paralleles ajoutees)
		# 3) l'arete choisie doit avoir le moins d'aretes paralleles sortantes (si elle etait consideree entrante), entrantes (si elle etait consideree sortante) totale

		aretesExt=[]
		if (aretesEntrantesChoisies):
			noeudsContenus += csr.getNoeudsPrecedents(noeudDepart) #noeuds lies au noeud de depart
			aretesExt = csr.getAretesParallelesSelonNoeudEntrantAretes(idAretesChoisies, True)
			# aretesExt += csr.getAretesSortantesNoeud(noeudDepart)
		else:
			noeudsContenus += csr.getNoeudsSuivants(noeudDepart) #noeuds lies au noeud de depart
			aretesExt = csr.getAretesParallelesSelonNoeudSortantAretes(idAretesChoisies, True)
			# aretesExt += csr.getAretesEntrantesNoeud(noeudDepart)

		nbRestantAretesPossibles = repartitionNbAretesSurProcs[numProc] - len(idAretesChoisies)
		while (nbRestantAretesPossibles > 0): #Tant que le proc peut prendre des aretes
			#Trouver les aretes candidates a etre ajoutees au proc
			aretesCandidatesAjout = {}
			for idNoeud in noeudsContenus:
				for idArete in csr.getAretesEntrantesNoeud(idNoeud):
					if (idArete not in aretesDejaChoisies and idArete not in idAretesChoisies and idArete not in aretesCandidatesAjout): #Si on trouve une arete candidate
						aretesCandidatesAjout[idArete] = "Entrante"
				for idArete in csr.getAretesSortantesNoeud(idNoeud):
					if (idArete not in aretesDejaChoisies and idArete not in idAretesChoisies and idArete not in aretesCandidatesAjout): #Si on trouve une arete candidate
						aretesCandidatesAjout[idArete] = "Sortante"

			# si aucune aretes candidates alors qu'il reste de la place (prendre des aretes non liees)
			if (len(aretesCandidatesAjout) == 0):
				for idArete in aretesRestantes:
					aretesCandidatesAjout[idArete] = "Non_liee"

			dictAretesAjoutes = {} #Pour chaque arete candidates, compter le nombre d'aretes ajoutees
			#TODO peut-etre considerer de verifier tous les groupes d'aretes, pas uniquement une par une
			#Compter le nombres d'aretes ajoutees pour chaque arete candidate
			for (idArete, etat) in aretesCandidatesAjout.items():
				noeud1Arete = None
				autreNoeudArete = None
				isAreteNonLiee = etat=="Non_liee"
				if etat=="Entrante":
					autreNoeudArete = csr.getNoeudEntrantArete(idArete)
				elif etat=="Sortante":
					autreNoeudArete = csr.getNoeudSortantArete(idArete)
				elif isAreteNonLiee:
					autreNoeudArete = csr.getNoeudEntrantArete(idArete)
					noeud1Arete = csr.getNoeudSortantArete(idArete)

				aretesParallelesAjoutees = csr.getAretesParallelesSelonNoeudSortantArete(idArete, True) + csr.getAretesParallelesSelonNoeudEntrantArete(idArete, True)
				for idArete2 in aretesParallelesAjoutees[::-1]:
					if (idArete2 in idAretesChoisies):
						aretesParallelesAjoutees.remove(idArete2)

				#Compter aussi le nombre de noeuds ajoutes (max 1 si une seule arete consideree)
				nbNoeudsAjoutes = 0
				noeudsAjoutes = []
				if (autreNoeudArete not in noeudsContenus):
					nbNoeudsAjoutes += 1
					noeudsAjoutes.append(autreNoeudArete)
				if isAreteNonLiee:
					nbNoeudsAjoutes += 1
					noeudsAjoutes.append(noeud1Arete)

				dictAretesAjoutes[idArete] = (aretesParallelesAjoutees, noeudsAjoutes)
				if len(aretesParallelesAjoutees)+len(noeudsAjoutes)==0:
					break

			#Parmi les aretes candidates, prendre le min
			min = None
			idAreteChoisie = None
			for (idArete, (aretesAjoutees, noeudsAjoutes)) in dictAretesAjoutes.items():

				tmpVal = len(aretesAjoutees)+len(noeudsAjoutes)
				if (min==None or tmpVal<min):
					min = tmpVal
					idAreteChoisie = idArete

			idAretesChoisies.append(idAreteChoisie) #TODO ajouter groupe d'aretes

			aretesExt += dictAretesAjoutes[idAreteChoisie][0]
			noeudsContenus += dictAretesAjoutes[idAreteChoisie][1]

			aretesRestantes.remove(idAreteChoisie)
			nbRestantAretesPossibles = repartitionNbAretesSurProcs[numProc] - len(idAretesChoisies)

		#Retraiter les valeurs dans aretesExt
		aretesExt = list(set(aretesExt)) #Supprimer doublons
		for idArete in aretesExt[::-1]: #Supprimer les aretes choisies dans le proc
			if idArete in idAretesChoisies:
				aretesExt.remove(idArete)

		aretesDejaChoisies += idAretesChoisies


		#Repartir les noeuds
		# Parmis les noeuds deja sensés etre recus du proc, on va choisir ceux qui peuvent etre traites par le proc
		# Ces choix vont se faire parmi un score
		#
		# Ajouter les noeuds dont un max d'aretes e/s sont deja dans le proc par les aretes paralleles
		# Priorites :
		# score +10)Ajouter les noeuds qui sont isoles au sein du proc (pas d'aretes ajoutees)
		# score  -1)Pour chaque arete exterieure ajoutee
		#
		# ?) ajouter des noeuds qui sont entre 2 procs et dont les procs sont deja traités
		# ?) Si des aretes e/s sont ajoutees, priviligier les noeuds dont un max d'aretes est deja dans le proc
		# TODO si plus aucun noeud possible alors qu'il reste de la place, on va devoir choisir des noeuds non lies au pack d'aretes

		#Choisir les scores des noeuds possibles à ajouter au traitement du proc
		noeudsChoisis = []
		noeudsPriorite={} # Dico {noeud : (score, [listeAretesSupp])} si score sup, ajouté au proc
		for idNoeud in noeudsContenus:
			if (idNoeud not in noeudsDejaChoisis):
				score = 0
				aretesExtSupplementaires = []
				if (idNoeud == noeudDepart):
					score += 1
				aretesNoeud = csr.getAretesEntrantesNoeud(idNoeud)
				aretesNoeud += csr.getAretesSortantesNoeud(idNoeud)
				nbAretesNonInclus = 0
				for idArete in aretesNoeud:
					if (not (idArete in idAretesChoisies or idArete in aretesExt)):
						aretesExtSupplementaires.append(idArete)
						nbAretesNonInclus += 1
				if (nbAretesNonInclus == 0):
					score += 10
				else :
					score -= nbAretesNonInclus
				noeudsPriorite[idNoeud]	= (score, aretesExtSupplementaires)

		#Choisir les noeuds suivant leur score
		for i in range(repartitionNbNoeudsSurProcs[numProc]):
			max = None
			noeudAjoute = None
			aretesExtSuppl = None
			for (noeud, (score, aretesExtSupplementaires)) in noeudsPriorite.items():
				if (max==None or score>max):
					max=score
					noeudAjoute = noeud
					aretesExtSuppl = aretesExtSupplementaires
			noeudsChoisis.append(noeudAjoute)
			if (noeudAjoute != None): # TODO etudier si ce cas est possible, on supposera pour l'instant qu'il n'est pas possible
				noeudsContenus.remove(noeudAjoute)
				noeudsPriorite.pop(noeudAjoute)
				noeudsDejaChoisis.append(noeudAjoute)
				aretesExt += aretesExtSuppl

		res.append((idAretesChoisies, aretesExt, noeudsChoisis, noeudsContenus))

	return res


#A partir d'une repartition de processeurs, cette fonction reaffine la structure pour ajouter les infos : qui recoit de qui, et qui envoit a qui ?
#Retourne
#	Pour chaque proc : 
#	([aretesATraiter], 
#	 {procX : [liste_Des_Aretes_A_Recevoir_De_ProcX], ...}
#	 {procX : [liste_Des_Aretes_A_Envoyer_A_ProcX], ...}
#	 [noeudsATraiter],
#	 {procX : [liste_Des_Noeuds_A_Recevoir_De_ProcX], ...}
#	 {procX : [liste_Des_Noeuds_A_Envoyer_A_ProcX], ...}
def mapsDesEchanges(repartition):
	res = []
	nbProc = len(repartition)
	aretesExtDemandeesParProc = [] # [[liste_Aretes_Ext_A_Recevoir_par_proc_0], ...]
	noeudsExtDemandeesParProc = [] # [[liste_Noeuds_Ext_A_Recevoir_par_proc_0], ...]
	for (_, aretesExtDemandees, _, noeudsExtDemandes) in repartition:
		aretesExtDemandeesParProc.append(aretesExtDemandees)
		noeudsExtDemandeesParProc.append(noeudsExtDemandes)

	#Creation des dicts des noeuds et aretes a recevoir
	listMapAretesARecevoir = [] #Pour chaque proc, dict des aretes a recevoir
	listMapNoeudsARecevoir = []
	for numProc in range(nbProc):
		mapAretes = {}
		mapNoeuds = {}
		# Pour chaque arete ext demandee, on va chercher quel autre processeur traite cette arete
		# et l'ajouter au dico des aretes_a_recevoir
		for areteDemandee in aretesExtDemandeesParProc[numProc]:
			for numProc2 in range(nbProc):
				if (numProc2 != numProc):
					for areteTraitee in repartition[numProc2][0]:
						if (areteDemandee==areteTraitee): #
							if (numProc2 in mapAretes):
								mapAretes[numProc2].append(areteDemandee)
							else:
								mapAretes[numProc2] = [areteDemandee]
							break
							break
		# Pour chaque noeud ext demande, on va chercher quel autre processeur traite ce noeud
		# et l'ajouter au dico des noeud_a_recevoir
		for noeudDemande in noeudsExtDemandeesParProc[numProc]:
			for numProc2 in range(nbProc):
				if (numProc2 != numProc):
					for noeudTraite in repartition[numProc2][2]:
						if (noeudDemande==noeudTraite):
							if (numProc2 in mapNoeuds):
								mapNoeuds[numProc2].append(noeudDemande)
							else:
								mapNoeuds[numProc2] = [noeudDemande]
							break
							break
		listMapAretesARecevoir.append(mapAretes)
		listMapNoeudsARecevoir.append(mapNoeuds)

	#Creation des dicts des noeuds et aretes a envoyer
	listMapAretesAEnvoyer = [] #Pour chaque proc, dict des aretes a envoyer
	listMapNoeudsAEnvoyer = []
	for numProc in range(nbProc):
		mapAretes = {}
		mapNoeuds = {}
		# On considère chaque proc (numProc)
		# On parcours les aretes que les autres procs (numProc2) doivent recevoir et on regarde qui doit recevoir du proc considéré (numProc3==numProc)
		# et on l'ajoute au dico des aretes à envoyer
		for numProc2 in range(nbProc):
			if (numProc != numProc2):
				for (numProc3, listeAretes) in listMapAretesARecevoir[numProc2].items():
					if (numProc3==numProc):
						if (numProc2 in mapAretes):
							mapAretes[numProc2] += listeAretes
						else:
							mapAretes[numProc2] = listeAretes
						break
		# On considère chaque proc (numProc)
		# On parcours les noeuds que les autres procs (numProc2) doivent recevoir et on regarde qui doit recevoir du proc considéré (numProc3==numProc)
		# et on l'ajoute au dico des noeuds à envoyer
		for numProc2 in range(nbProc):
			if (numProc != numProc2):
				for (numProc3, listeNoeuds) in listMapNoeudsARecevoir[numProc2].items():
					if (numProc3==numProc):
						if (numProc2 in mapNoeuds):
							mapNoeuds[numProc2] += listeNoeuds
						else:
							mapNoeuds[numProc2] = listeNoeuds
						break
		listMapAretesAEnvoyer.append(mapAretes)
		listMapNoeudsAEnvoyer.append(mapNoeuds)

	for numProc in range(nbProc):
		res.append((repartition[numProc][0], listMapAretesARecevoir[numProc], listMapAretesAEnvoyer[numProc], repartition[numProc][2], listMapNoeudsARecevoir[numProc], listMapNoeudsAEnvoyer[numProc]))
	return res

# Remet dans l'ordre les elements a traiter pour chaque processeur (noeuds : [locaux-internes | locaux-externes | feuilles | racines | noeuds-externes])
def setRepartitionOrdonnee(repartition, csr):

	listIndexTypeNoeuds = [] # Liste qui servira a stocker les index du debut de chaque type de noeud
	listRepartitionOrdonnee = []
	listIndexTypeAretes = []
	listAretesOrdonnee = []

	for (aretesATraiter, aretesExt, noeudsATraiter, noeudsExt) in repartition:
		l_locaux_int = []
		l_locaux_ext = []
		l_feuilles = []
		l_racines = []
		for noeud in noeudsATraiter:
			#Si c'est une racine
			if noeud in csr.getNoeudsRacines():
				l_racines.append(noeud)
			#Si c'est une feuille
			elif noeud in csr.getNoeudsFeuilles():
				l_feuilles.append(noeud)
			#Si c'est un local interne ou un local externe
			else:
				#test local externe ou interne si une seule arete sortante ou entrante d'un noeud n'est pas dans
				# la liste des aretes a traiter, ce noeud est local externe
				a_entrantes = csr.getAretesEntrantesNoeud(noeud)
				a_sortantes = csr.getAretesSortantesNoeud(noeud)
				testAretesPresentes = a_entrantes + a_sortantes
				for arete in aretesATraiter:
					for i in range(0, len(testAretesPresentes)):
						if testAretesPresentes[i] == arete:
							testAretesPresentes.pop(i)
							break
				if not testAretesPresentes: #Si le tableau a été vidé
					l_locaux_int.append(noeud)
				else:
					l_locaux_ext.append(noeud)

		taille_li = len(l_locaux_int)
		taille_le = len(l_locaux_ext)
		taille_lf = len(l_feuilles)
		taille_lr = len(l_racines)
		taille_lne= len(noeudsExt)
		#Tableau utile pour parcourir un type de noeuds une fois que tout est fusionne
		listIndexTypeNoeuds.append([ taille_li,
		                        taille_li + taille_le,
		                        taille_li + taille_le + taille_lf,
		                        taille_li + taille_le + taille_lf + taille_lr,
		                        taille_li + taille_le + taille_lf + taille_lr + taille_lne
		                        ])

		# Tableau final ordonne par type de noeud
		listRepartitionOrdonnee.append( l_locaux_int + l_locaux_ext + l_feuilles + l_racines + noeudsExt )

		# Aretes :
		taille_a_int = len(aretesATraiter)
		taille_a_ext = len(aretesExt)
		listIndexTypeAretes.append([taille_a_int, taille_a_int + taille_a_ext])

		listAretesOrdonnee.append(aretesATraiter + aretesExt)
	###
	return listRepartitionOrdonnee, listAretesOrdonnee, listIndexTypeNoeuds, listIndexTypeAretes

# Retourne les mini-csr pour chaque proc
# Retourne une liste de taile nb_proc : [mini_csr pour proc0, mini_csr pour proc1, ...]
def reconstituerCsr(repartitionNoeud, repartitionArete, csr, listIndexTypeNoeuds):
	res = []
	for num_proc in range(0, len(repartitionNoeud)):# Pour chaque proc
		# On va recalculer a la main toutes les listes csr necessaires pour le mini_csr
		refersNoeuds = repartitionNoeud[num_proc]
		refersAretes = repartitionArete[num_proc]
		index_as = [0]
		voisins_as = []
		index_ae = [0]
		voisins_ae = []
		voisins_ns = []
		voisins_ne = []
		noeudsExt = refersNoeuds[listIndexTypeNoeuds[num_proc][3]:]
		# Avec chaque noeuds, on va recreer les listes de CSR
		for newIdNoeud in range(len(refersNoeuds)):
			idNoeud = refersNoeuds[newIdNoeud]
			aretesSortantes = csr.getAretesSortantesNoeud(idNoeud)
			aretesEntrantes = csr.getAretesEntrantesNoeud(idNoeud)
			#On supprime toutes les aretes  non-incluses dans le proc


			if (idNoeud in noeudsExt):
				for idArete in aretesSortantes[::-1]:
					if (idArete not in refersAretes):
						aretesSortantes.remove(idArete)
				for idArete in aretesEntrantes[::-1]:
					if (idArete not in refersAretes):
						aretesEntrantes.remove(idArete)

			#On recupere les noeuds, on remplace les noeuds fictifs par des -1, et on reindexe les noeuds en fonction de references
			for idArete in aretesSortantes:
				noeudSortant = csr.getNoeudSortantArete(idArete)
				if (noeudSortant in refersNoeuds):
					voisins_ns.append(refersNoeuds.index(noeudSortant))
				else:
					voisins_ns.append(-1)
			for idArete in aretesEntrantes:
				noeudEntrant = csr.getNoeudEntrantArete(idArete)
				if (noeudEntrant in refersNoeuds):
					voisins_ne.append(refersNoeuds.index(noeudEntrant))
				else:
					voisins_ne.append(-1)

			#Reindexer en fonction des references refersAretes
			for i in range(len(aretesSortantes)):
				aretesSortantes[i] = refersAretes.index(aretesSortantes[i])
			for i in range(len(aretesEntrantes)):
				aretesEntrantes[i] = refersAretes.index(aretesEntrantes[i])

			# On ajoute les aretes reindexees aux listes
			index_as.append(index_as[-1]+len(aretesSortantes))
			voisins_as += aretesSortantes
			index_ae.append(index_ae[-1]+len(aretesEntrantes))
			voisins_ae += aretesEntrantes

		# On informe le mini_csr quels noeuds sont racines/feuille/internes, et on lui informe des valeurs
		racines = []
		internes = []
		feuilles = []
		valeursNoeuds = []
		valeursAretes = []
		for newIdNoeud in range(len(refersNoeuds)):
			idNoeud = refersNoeuds[newIdNoeud]
			if (idNoeud in csr.getNoeudsRacines()):
				racines.append(newIdNoeud)
			elif (idNoeud in csr.getNoeudsFeuilles()):
				feuilles.append(newIdNoeud)
			else:
				internes.append(newIdNoeud)
			valeursNoeuds.append(csr.getValeurNoeud(idNoeud)) #TODO peut-etre ne pas enregistrer les valeurs des noeuds externes
		for newIdArete in range(len(refersAretes)):
			idArete = refersAretes[newIdArete]
			valeursAretes.append(csr.getValeurArete(idArete)) #TODO peut-etre ne pas enregistrer les valeurs des aretes externes

		mini_csr = CSR(refersNoeuds, valeursNoeuds, index_as, voisins_ns, valeursAretes, racines, feuilles, internes, index_ae, voisins_ne, voisins_as, voisins_ae, refersAretes)
		res.append(mini_csr)
	return res