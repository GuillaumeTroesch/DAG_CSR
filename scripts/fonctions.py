from math import *


#flotRacine :
#parametres : temps t et nom de noeud
#sortie : entier a affecter au noeud

#return 4 si noeud pair, t+1 si noeud impair
def flotRacine1(temps, noeud):
	if (noeud%2==0):
		return 4
	else :
		return temps+1

#return l'id du noeud + 1
def floatRacine2(temps, noeud):
	return noeud+1

#return 4,3,2,1,0,1,2,3,4,3...
def flotRacine3(temps, noeud):
	return round(2*cos(temps*pi/4))+2
	
#return toujours 5
def flotRacine4(temps, noeud):
	return 5
	
#return 10 au debut, puis toujours 0
def flotRacine5(temps, noeud):
	if temps==0:
		return 10
	return 0	
	


#ecoulementFeuille
#parametres : temps t, nom de noeud, flot actuel du noeud
#sortie : entier a retirer du noeud

#vide entierement la feuille
def ecoulementFeuille1(temps, noeud, flotNoeud):
	return flotNoeud

#vide la feuille de 2 unites
def ecoulementFeuille2(temps, noeud, flotNoeud):
	return 2

#retire 2, puis 1 alternativement
# def ecoulementFeuille3(temps, noeud, flotNoeud):
	# return flotNoeud-int(cos(temps*pi)+4)//2

#ne retire rien
def ecoulementFeuille4(temps, noeud, flotNoeud):
	return 0
	
	
def getFlot(item):
	return item[0]
	
def getCapacite(item):
	return item[1]

#calcul de la valeur d'un noeud
#parametres : temps t, 
#		nom du noeud, 
#		liste des aretes entrantes de la forme [(flot, capacite), ...], 
#		noeud de la forme (flot, capacite), 
#		liste des aretes sortantes de la forme [(flot, capacite), ...]
#sortie : nouvelle valeur du noeud

#prendre tout equitablement, redonner tout equitablement
def fctNoeuds1(temps, idNoeud, dag):
	aretesEntrantes = dag.getValeursAretes(dag.getAretesEntrantesNoeud(idNoeud))
	noeud = dag.getValeurNoeud(idNoeud)
	aretesSortantes = dag.getValeursAretes(dag.getAretesSortantesNoeud(idNoeud))
	res = getFlot(noeud)
	
	#Le noeud prend tout ce qu'il peut des aretes
	somme1 = 0
	for (flot, _) in aretesEntrantes:
		somme1 += flot
		if (getCapacite(noeud)-getFlot(noeud)<=somme1): #si la somme depasse, inutile de continuer a compter
			break
	res += min(somme1, getCapacite(noeud)-getFlot(noeud))
	
	#Le noeud redonne tout ce qu'il peut aux aretes
	somme2 = 0
	for (flot, capacite) in aretesSortantes:
		somme2 += (capacite-flot)
		if (getFlot(noeud)<=somme2): #si la somme depasse, inutile de continuer a compter
			break
	res -= min(getFlot(noeud), somme2)
	return res
	

	
	
#calcul de la valeur d'une arete
#parametres : temps t, 
#		noeudEntrant de la forme (flot, capacite), 
#		liste des aretes sortantes du meme noeud de la forme [(flot, capacite),..]
#		indice de l'arete consideree dans cette liste
#		liste des aretes entrante du meme noeud de la forme [(flot, capacite),..]
#		indice de l'arete consideree dans cette liste
#		noeudSortant de la forme (flot, capacite)
#sortie : nouvellevaleur de l'arete
	
#prendre des aretes equitablement et redonner equitablement
def fctArete1(temps, idArete, dag):
	arete = dag.getValeurArete(idArete)
	idNoeudEntrant = dag.getNoeudEntrantArete(idArete)
	idNoeudSortant = dag.getNoeudSortantArete(idArete)
	noeudEntrant = dag.getValeurNoeud(idNoeudEntrant)
	noeudSortant = dag.getValeurNoeud(idNoeudSortant)
	idsAretesSortantes = dag.getAretesSortantesNoeud(idNoeudEntrant)
	aretesParalellesSortantes = dag.getValeursAretes(idsAretesSortantes)
	idsAretesEntrantes = dag.getAretesEntrantesNoeud(idNoeudSortant)
	aretesParallesEntrantes = dag.getValeursAretes(idsAretesEntrantes)
	indice1 = idsAretesSortantes.index(idArete)
	indice2 = idsAretesEntrantes.index(idArete)
	
	tmp_res_1 = 0
	tmp_res_2 = 0
	
	#prendre equitablement
	tmp_capacites = []
	for (flot, capacite) in aretesParalellesSortantes:
		tmp_capacites.append(capacite-flot)
		
	capacite_restante = getCapacite(arete)-getFlot(arete)
	flotEntrant = getFlot(noeudEntrant)
	while(capacite_restante>0 and flotEntrant>0 and len(tmp_capacites)>0): #Tant qu'on trouve un min qui est inferieur au flot qui peut etre reparti
		capacite_min = min(tmp_capacites)
		ind_flot_min = tmp_capacites.index(capacite_min)
		capacite_min_all = capacite_min*len(tmp_capacites)
		if (ind_flot_min==indice1 and capacite_min_all<flotEntrant): #Si le min trouve est l'arete etudiee et que ce min peut etre mis toutes les aretes, on sait que cette arete va etre remplie
			tmp_res_1=getCapacite(arete)-getFlot(arete)
			break
		elif (capacite_min_all < flotEntrant): #On enleve le min de la liste, et on continue de chercher
			if (tmp_capacites.index(capacite_min)<indice1):
				indice1-=1
			tmp_capacites.remove(capacite_min)
			flotEntrant -= capacite_min
		else: #Si le flot qui peut etre reparti est plus petit que les capacites des aretes restantes de la liste, on le divise sur les aretes restantes
			tmp_res_1 = flotEntrant // len(tmp_capacites)
			if (flotEntrant%len(tmp_capacites)>=indice1+1):
				tmp_res_1+=1
			break
	if (len(tmp_capacites)==0): #Si on a supprime tous les min de la liste, ca signifie que le flot est superieur a toutes les capacites sommees
		tmp_res_1=getCapacite(arete)
			
	#donner equitablement
	tmp_flots = []
	for (flot, capacite) in aretesParallesEntrantes:
		tmp_flots.append(flot)
	capacite_sortante = getCapacite(noeudSortant)-getFlot(noeudSortant)
	
	while (capacite_sortante>0 and getFlot(arete)>0 and len(tmp_flots)>0): #Tant qu'on trouve un min qui peut etre donne entierement au noeud sortant
		flot_min = min(tmp_flots)
		ind_flot_min = tmp_flots.index(flot_min)
		flot_min_all = flot_min*len(tmp_flots)
		if (ind_flot_min==indice2 and flot_min_all<capacite_sortante): #Si le min trouve est l'arete etudiee et que ce min est repartissable sur toutes les aretes, on sait que cette arete va etre videe
			tmp_res_2 = getFlot(arete)
			break
		elif (flot_min_all<capacite_sortante): #Si le min est repartissable sur toutes les aretes, on supprime le min de la liste et on continue de chercher
			if (tmp_flots.index(flot_min)<indice2):
				indice2-=1
			tmp_flots.remove(flot_min)
			capacite_sortante-=flot_min
		else: #Si le min n'est pas repartissable, on le divise en parts egales
			tmp_res_2 = capacite_sortante // len(tmp_flots)
			if (capacite_sortante%len(tmp_flots)>=indice2+1):
				tmp_res_2+=1
			break
	
	return getFlot(arete) + tmp_res_1 - tmp_res_2
