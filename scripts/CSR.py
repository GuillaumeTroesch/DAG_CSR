class CSR:

	def __init__(self, noeuds, valeurnoeuds, index_ns, voisins_ns, valeuraretes, listracines=None, listinternes=None, listfeuilles=None, index_ne=None, voisins_ne=None, voisins_as=None, voisins_ae=None, correspondancesAretes=None):
		self.noeuds=noeuds # liste des noms des noeuds : ["0", "1", ...] #Sert aussi pour la correspondance des mini-CSR sur chaque proc : [17, 19, 20, ...] sur grand-csr correspondent a [0, 1, 2,..] sur mini-csr
		self.valeurnoeuds = valeurnoeuds # liste des (flot, capacite) des noeuds : [(0, 10), (3, 15), ...]
		self.correspondancesAretes = correspondancesAretes #Sert pour la correspondance des aretes des mini-CSR sur chaque proc : [17, 19, 20, ...] sur grand-csr correspondent a [0, 1, 2,..] sur mini-csr
		self.valeuraretes=valeuraretes # liste des (flot, capacite) des aretes : [(1, 4), (0, 9), ...]

		# Rappelons que index_as=index_ns
		# et index_ae=index_ne
		self.index_as = index_ns #tableau des degres cumulatifs des aretes sortantes : cdeg+
		self.index_ae = [] #tableau des degres cumulatifs des aretes entrantes : cdeg-
		self.voisins_as = [] #tableau des index des aretes sortantes : Ne+
		self.voisins_ae = [] #tableau des index des aretes entrantes : Ne-
		self.sommets_fils = voisins_ns #tableau des sommets fils : D #voisins_ns
		self.sommets_parents = [] #tableau des sommets parents : S #voisins_ne 
		
		if (index_ne==None):
			self.setList()
		else:
			self.index_ae = index_ne
			self.voisins_as = voisins_as
			self.voisins_ae = voisins_ae
			self.sommets_parents = voisins_ne
		
		if (listfeuilles==None):
			self.listfeuilles = []
			self.initListFeuilles()
		else:
			self.listfeuilles=listfeuilles # liste des noeuds feuilles : [4, 5, 10, 11, ...]

		if (listracines==None):
			self.listracines = []
			self.initListRacines()
		else:
			self.listracines=listracines # liste des noeuds racines : [0, 1, ...]

		if (listinternes==None):
			self.listinternes = []
			self.initListInternes()
		else:
			self.listinternes=listinternes # liste des noeuds internes : [2, 3, 6, ...]
			
	#Initalise les listes de la structure de données
	def setList(self):
		for i in range(0, len(self.sommets_fils)):
			self.voisins_as.append(i)

		#Initialisation du tableau des sommets_parents <==> S			
		for idNoeud in range(len(self.noeuds)):
			for i in range(len(self.sommets_fils)):
				if (self.sommets_fils[i]==idNoeud):
					for x in range(len(self.index_as)):
						if (self.index_as[x]==i):
							self.sommets_parents.append(x)
							break
						if (self.index_as[x]>i):
							self.sommets_parents.append(x-1)
							break
			

		self.index_ae.append(0)
		#Initialisation du tableau cdeg-
		compteur_sommet = 0
		for i in range(0, len(self.index_as)-1):
			for index_s in self.sommets_fils:
				if index_s == i:
					compteur_sommet += 1

			self.index_ae.append(compteur_sommet)
			
		#Initialisation tableau Ne-			
		for idNoeud in range(len(self.noeuds)):
			for i in range(len(self.sommets_fils)):
				if (self.sommets_fils[i]==idNoeud):
					self.voisins_ae.append(i)
			
	def setValeurNoeud(self, indiceNoeud, newValeurNoeud):
		self.valeurnoeuds[indiceNoeud] = newValeurNoeud

	def setValeurArete(self, indiceArete, newValeurArete):
		self.valeuraretes[indiceArete] = newValeurArete

	#Set valeurnoeuds
	def setValeursNoeuds(self, newValeurNoeuds):
		self.valeurnoeuds = newValeurNoeuds

	def setValeursAretes(self, newValeurAretes):
		self.valeuraretes = newValeurAretes

	#Retourne liste des noms des noeuds
	def getNoeuds(self):
		return self.noeuds
		
	#Retourne liste des nums des noeuds
	def getNumsNoeuds(self):
		return list(range(len(self.noeuds))) # egale aussi à range(len(self.valeurnoeuds))
	
	#Retourne liste des (flot, capacite) des noeuds
	def getValeurNoeuds(self):
		return self.valeurnoeuds
	
	#Retourne liste des nums des noeuds feuilles
	def getNoeudsFeuilles(self):
		return self.listfeuilles

	#Retourne liste des nums des noeuds racines
	def getNoeudsRacines(self):
		return self.listracines

	#Retourne liste des nums des noeuds internes
	def getNoeudsInternes(self):
		return self.listinternes
	
	#Retourne liste des nums des aretes
	def getNumAretes(self):
		return list(range(len(self.valeuraretes)))
		
	# param : int num d'arete (si non renseigne, donne toutes les aretes)
	# sortie : liste des (flot, capacite) des aretes
	def getValeursAretes(self, idAretes=False):
		if not idAretes and idAretes != []:
			return list(self.valeuraretes)
		res = []
		for id in idAretes:
			res.append(self.valeuraretes[id])
		return res
	
	def getNbAretes(self):
		return len(self.valeuraretes)
		
	def getNbNoeuds(self):
		return len(self.valeurnoeuds)
		
		
		
	#Retourne nom de noeud
	def getNomNoeud(self, numNoeud):
		return self.noeuds[numNoeud]

	# Pour les csr locaux
	def getNumNoeud(self, nomNoeud):
		return self.noeuds.index(nomNoeud)

	#Retourne (flot, capacite) de noeud
	def getValeurNoeud(self, numNoeud):
		return self.valeurnoeuds[numNoeud]
		
	#Retourne (flot, capacite) de noeud
	def getValeurNoeudByName(self, nomNoeud):
		if nomNoeud not in self.noeuds:
			return -1
		return self.valeurnoeuds[self.noeuds.index(nomNoeud)]

	#Retourne (flot, capacite) de valeur
	def getValeurArete(self, idArete):
		return self.valeuraretes[idArete]
	
	#Retourne (flot, capacite) de noeud
	def getValeurAreteByName(self, numArete):
		if numArete not in self.correspondancesAretes:
			return -1
		return self.valeuraretes[self.correspondancesAretes.index(numArete)]

	def getIndexAreteByName(self, numArete):
		return self.correspondancesAretes.index(numArete)

	# param : int num du noeud
	# sortie : liste des id des aretes entrantes
	def getAretesEntrantesNoeud(self, idNoeud):
		return self.voisins_ae[self.index_ae[idNoeud]:self.index_ae[idNoeud+1]]
		
	# param : idNoeud
	# sortie : nb d'aretes entrantes du noeud
	def getNbAretesEntrantesNoeud(self, idNoeud):
		return self.index_ae[idNoeud+1] - self.index_ae[idNoeud]
		
	# param : int num du noeud
	# sortie : liste des id des aretes sortantes
	def getAretesSortantesNoeud(self, idNoeud):
		return self.voisins_as[self.index_as[idNoeud]:self.index_as[idNoeud+1]]
		
	# param : idNoeud
	# sortie : nb d'aretes sortantes du noeud
	def getNbAretesEntrantesNoeud(self, idNoeud):
		return self.index_as[idNoeud+1] - self.index_as[idNoeud]
	


	# param : id de arete
	# sortie : id du noeud entrant
	def getNoeudEntrantArete(self, idArete):
		pos = self.voisins_as.index(idArete)
		for x in range(len(self.index_as)):
			if (self.index_as[x]>pos):
				return x-1
	
	# param : id de arete
	# sortie : id du noeud sortant
	def getNoeudSortantArete(self, idArete):
		pos = self.voisins_ae.index(idArete)
		for x in range(len(self.index_ae)):
			if (self.index_ae[x]>pos):
				return x-1
		
	# param : int num de noeuds
	# sortie : liste des (flot, capacite) des aretes
	def getValeursNoeuds(self, idNoeuds):
		res = []
		for id in idNoeuds:
			res.append(self.valeurnoeuds[id])
		return res
		
	
	# param : int num du noeud
	# sortie : liste des noeuds precedents du noeud : [3, 4, ...]
	def getNoeudsPrecedents(self, idNoeud):
		return self.sommets_parents[self.index_ae[idNoeud] : self.index_ae[idNoeud+1]]
	
	# param : int num du noeud
	# sortie : liste des noeuds suivants du noeud : [3, 4, ...]
	def getNoeudsSuivants(self, idNoeud):
		return self.sommets_fils[self.index_as[idNoeud] : self.index_as[idNoeud+1]]
		
	
	
	# param : idArete et bool si le res ne doit pas contenir idArete
	# sortie : liste des aretes paralleles a idArete en prenant le noeud entrant comme reference
	def getAretesParallelesSelonNoeudEntrantArete(self, idArete, removeIdArete=False):
		idNoeudEntrant = self.getNoeudEntrantArete(idArete)
		aretesSortantes = self.getAretesSortantesNoeud(idNoeudEntrant)
		if (not removeIdArete):
			return aretesSortantes
		aretesSortantes.remove(idArete)
		return aretesSortantes	

	# param : idArete et bool si le res ne doit pas contenir idArete
	# sortie : liste des aretes paralleles a idArete en prenant le noeud sortant comme reference
	def getAretesParallelesSelonNoeudSortantArete(self, idArete, removeIdArete=False):
		idNoeudSortant = self.getNoeudSortantArete(idArete)
		aretesEntrantes = self.getAretesEntrantesNoeud(idNoeudSortant)
		if (not removeIdArete):
			return aretesEntrantes
		aretesEntrantes.remove(idArete)
		return aretesEntrantes


	def getAretesParallelesSelonNoeudSortantAretes(self, idAretes, removeIdAretes=False):
		res = []
		for idArete in idAretes:
			for newIdArete in self.getAretesParallelesSelonNoeudSortantArete(idArete):
				if (newIdArete not in res and (not removeIdAretes or newIdArete not in idAretes)):
					res.append(newIdArete)
		return res
		
	def getAretesParallelesSelonNoeudEntrantAretes(self, idAretes, removeIdAretes=False):
		res = []
		for idArete in idAretes:
			for newIdArete in self.getAretesParallelesSelonNoeudEntrantArete(idArete):
				if (newIdArete not in res and (not removeIdAretes or newIdArete not in idAretes)):
					res.append(newIdArete)
		return res


	def initListFeuilles(self):
		for i in range(0, len(self.index_as)-1):
			if self.index_as[i] == self.index_as[i+1]:
				self.listfeuilles.append(i)

	def initListRacines(self):
		for i in range(0, len(self.index_ae)-1):
			if self.index_ae[i] == self.index_ae[i+1]:
				self.listracines.append(i)

	def initListInternes(self):
		for i in range(len(self.noeuds)):
			if (i not in self.listfeuilles and i not in self.listracines):
				self.listinternes.append(i)

	
	def appliquerFctRacine(self, fctRacine, temps):
		for id in self.getNoeudsRacines():
			self.valeurnoeuds[id]=(min(fctRacine(temps, self.getNomNoeud(id)), self.valeurnoeuds[id][1]), self.valeurnoeuds[id][1])
		return 0


	def afficher(self):
		# print("Noeuds :")
		# print(self.noeuds)
		print("Valeurs Noeuds : ")
		print(self.valeurnoeuds)
		# print("Liste 1 CSR : ")
		# print(self.index)
		# print("Liste 2 CSR (Voisins) : ")
		# print(self.voisins)
		print("Valeurs aretes : ")
		print(self.valeuraretes)
		# print("Indices Aretes parentes")
		# print(self.listparentsedge)
		# print("Test Flot arete")
		# print(self.getFlotAretesE(7))
		# print("Test capacites sortants")
		# print(self.getCapaciteAretesS(9))
		
		# print()
		# print("Index des noeuds sortants (index_as) (cdeg+)")
		# print(self.index_as)
		# print("Voisins des noeuds sortants (sommets_fils) (D)")
		# print(self.sommets_fils)
		# print("Index des aretes entrantes (index_ae) (cdeg-)")
		# print(self.index_ae)
		# print("Voisins des aretes entrantes (voisins_ae) (NE-)")
		# print(self.voisins_ae)
		# print("Index des aretes sortantes (index_as) (cdeg+)")
		# print(self.index_as)
		# print("Voisins des aretes sortantes (voisins_as) (NE+)")
		# print(self.voisins_as)
		# print("Index des noeuds entrants (index_ae) (cdeg-)")
		# print(self.index_ae)
		# print("Voisins des noeuds entrants (sommets_parents) (S)")
		# print(self.sommets_parents)
		# print()
	
	def __str__(self):
		return "<Object CSR, "+str(self.getNbNoeuds())+" noeuds, "+str(self.getNbAretes())+" aretes>"
	
