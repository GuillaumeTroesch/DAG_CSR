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
#sortie : entier a affecter au noeud

#vide entierement la feuille
def ecoulementFeuille1(temps, noeud, flotNoeud):
	return 0

#vide la feuille de 2 unites
def ecoulementFeuille2(temps, noeud, flotNoeud):
	return flotNoeud-2

#retire 2, puis 1 alternativement
# def ecoulementFeuille3(temps, noeud, flotNoeud):
	# return flotNoeud-int(cos(temps*pi)+4)//2

#ne retire rien
def ecoulementFeuille4(temps, noeud, flotNoeud):
	return flotNoeud
	
	
	
#separationNoeud
#parametres : temps t, nom noeud, flot actuel du noeud, capacite max des aretes sortantes du noeud
#sortie : tuple :
#	0 : flot final du noeud
#	1 : tableau de taille nbAretesSortantes, de valeurs la repartition du flot dans chaque arete sortante


#tout sur les premieres aretes
def separationNoeud1(temps, noeud, flotNoeud, capaciteAretesSortantes):
	res = []
	for capacite in capaciteAretesSortantes:
		if (flotNoeud > capacite):
			res.append(capacite)
			flotNoeud-=capacite
		else:
			res.append(flotNoeud)
			flotNoeud=0
	return (flotNoeud, res)

#equitablement
#CETTE FONCTION N'EST PAS AU POINT
def separationNoeud2(temps, noeud, flotNoeud, capaciteAretesSortantes):
	res = [0]*len(capaciteAretesSortantes)
	modif = True #modif si les aretes ne sont pas satures
	i=0
	while (flotNoeud>0 and modif):
		if (i>=len(capaciteAretesSortantes)):
			modif = False
			i=0
		if (capaciteAretesSortantes[i]>res[i]):
			res[i]+=1
			flotNoeud-=1
			modif=True
		i+=1

	return (flotNoeud, res)

#equitablement 2
def separationNoeud3(temps, noeud, flotNoeud, capaciteAretesSortantes):
	tmp_capacites = list(capaciteAretesSortantes)
	nbAretesSortantes = len(capaciteAretesSortantes)
	tmp_nbAretesSortantes = nbAretesSortantes
	res = [0]*nbAretesSortantes

	somme=0
	for capacite in capaciteAretesSortantes:
		somme+=capacite
	if (flotNoeud>=somme):
		return (flotNoeud-somme, capaciteAretesSortantes)
		
	#Si flotNoeud < somme des capacite
	#On va d'abord prendre le min des capacites sortantes, verifier que l'on peut mettre le flotNoeud dans chaque noeud avec ce min.
	#Tant qu'on peut faire ca, on ajoute le min, et on reduit le flotNoeud a separer.
	#Si flotNoeud est inferieur au min repartissable sur chaque arete, on divise (div Entiere) flotNoeud par le nombre de noeuds et on remplit les aretes par cette valeur
	#Si flotNoeud est inferieur au nombre d'aretes, on remplit les aretes de 1 en commencant par la gauche
	while (flotNoeud>0):
		capacite_minimale = min(tmp_capacites)
		if (flotNoeud>=capacite_minimale*tmp_nbAretesSortantes): #si le flot du noeud peut couvrir toutes les aretes avec un flot de valeur capacite_minimale
			for i in range(nbAretesSortantes): #on remplit toutes les aretes avec un flot capacite_minimale, si l'arete n'est pas deja saturee
				if (capaciteAretesSortantes[i]!=res[i]):
					res[i]+=capacite_minimale
			flotNoeud-=capacite_minimale*tmp_nbAretesSortantes #on diminue le flot du noeud a repartir

			tmp_capacites.remove(capacite_minimale) #on enleve les noeuds satures
			tmp_nbAretesSortantes=len(tmp_capacites)
			for i in range(len(tmp_capacites)):
				tmp_capacites[i]-=capacite_minimale
		else: #si le flot du noeud est trop petit pour couvrir toutes les aretes avec un flot de valeur capacite_minimale 
			if (flotNoeud >= tmp_nbAretesSortantes): #si flotNoeud est divisible par les aretes sortantes
				flot_ajoute = flotNoeud//tmp_nbAretesSortantes
				for i in range(nbAretesSortantes): #on remplit toutes les aretes avec un flot separe equitablement, si l'arete n'est pas deja saturee
					if (capaciteAretesSortantes[i]>=res[i]+flot_ajoute and flot_ajoute>0):
						res[i] += flot_ajoute
						flotNoeud-=flot_ajoute
			else: #Si flotNoeud est plus petit que le nb d'aretes sortantes
				j=0
				i=0
				while(flotNoeud>0 and j<tmp_nbAretesSortantes): #On separe le reste du flot qui est inferieur a tmp_nbAretesSortantes
					if (capaciteAretesSortantes[i]>res[i]):
						res[i]+=1
						j+=1
						flotNoeud-=1
					i+=1

	return (flotNoeud, res)

#Ne donner que 1 a chaque arete
def separationNoeud4(temps, noeud, flotNoeud, capaciteAretesSortantes):
	res = []
	for capacite in capaciteAretesSortantes:
		if (capacite>0 and flotNoeud>0):
			res.append(1)
			flotNoeud-=1
		else:
			res.append(0)
	return (flotNoeud, res)
	
#Au temps 1, Ne donner que 1 a chaque arete
#sinon repartir tout equitablement
def separationNoeud5(temps, noeud, flotNoeud, capaciteAretesSortantes):
	if (temps%2==1):
		return separationNoeud4(temps, noeud, flotNoeud, capaciteAretesSortantes)
	return separationNoeud3(temps, noeud, flotNoeud, capaciteAretesSortantes)



#accumulationNoeud
#parametres : temps t, nom noeud, flot max du noeud, flot actuel des aretes entrantes du noeud
#sortie :
#	0 : float final du noeud
#	1 : tableau de taille nbAretesEntrantes, de valeurs la repartition du flot dans chaque arete entrante

#tout pris des premieres aretes
def accumulationNoeud1(temps, noeud, capaciteNoeud, flotAretesEntrantes):
	nbAretesEntrantes = len(flotAretesEntrantes)
	res = flotAretesEntrantes
	flotNoeud=0
	i=0
	while (capaciteNoeud>flotNoeud and i<nbAretesEntrantes):
		cur_flotAretesEntrante = flotAretesEntrantes[i]
		if (capaciteNoeud>flotNoeud+cur_flotAretesEntrante):
			res[i]=0
			flotNoeud+=cur_flotAretesEntrante
		else:
			res[i]=cur_flotAretesEntrante-(capaciteNoeud-flotNoeud)
			flotNoeud=capaciteNoeud
		i+=1
	return (flotNoeud, res)

#equitablement
#CETTE FONCTION N'EST PAS AU POINT
def accumulationNoeud2(temps, noeud, capaciteNoeud, flotAretesEntrantes):
	nbAretesEntrantes = len(flotAretesEntrantes)
	res = flotAretesEntrantes
	flotNoeud=0
	i=0
	modif = True #modif si les aretes ne sont pas vides
	while (capaciteNoeud>flotNoeud and modif):
		if (i>=nbAretesEntrantes):
			i=0
			modif=False
		if (res[i]>0):
			res[i]-=1
			flotNoeud+=1
			modif=True
		i+=1
	return (flotNoeud, res)

#equitablement 2
#CETTE FONCTION N'EST PAS AU POINT
def accumulationNoeud3(temps, noeud, capaciteNoeud, flotAretesEntrantes):
	pass #TODO avec min
	
#ne prendre que 1 de chaque arete
def accumulationNoeud4(temps, noeud, capaciteNoeud, flotAretesEntrantes):
	res = []
	flotNoeud=0
	for flotE in flotAretesEntrantes:
		if (flotNoeud<capaciteNoeud and flotE>0):
			res.append(flotE-1)
			flotNoeud+=1
		else:
			res.append(flotE)
	return (flotNoeud, res)
		


#TESTS
# for i in range(10):
	# print(ecoulementFeuille3(i, 0, 4))

# print(separationNoeud1(0, 0, 21, [5,3,4,2,5,6,4]))
# print(separationNoeud2(0, 0, 21, [5,3,4,2,5,6,4]))
# print(separationNoeud3(0, 0, 2102, [500, 300,400,200,500,600,319]))

# print(separationNoeud2(0, 0, 5, [1,1,1,4]))

# print(accumulationNoeud1(0, 0, 21, [5,3,4,2,5,6,4]))
# print(accumulationNoeud1(0, 0, 21, [5,3]))
# print(accumulationNoeud2(0, 0, 21, [5,3,4,2,5,6,4]))
# print(accumulationNoeud2(0, 0, 21, [5,3]))



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

#prendre tout en partant des premieres aretes et redonner tout en remplissant les premieres aretes
def fctNoeuds1(temps, nomNoeud, aretesEntrantes, noeud, aretesSortantes):
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
	
#prendre tout equitablement, redonner tout equitablement
#en fait c'est la meme que fctNoeuds1
def fctNoeuds2(temps, nomNoeud, aretesEntrantes, noeud, aretesSortantes):
	return fctNoeuds1(temps, nomNoeud, aretesEntrantes, noeud, aretesSortantes)
	

	
	
#calcul de la valeur d'une arete
#parametres : temps t, 
#		noeudEntrant de la forme (flot, capacite), 
#		liste des aretes sortantes du meme noeud de la forme [(flot, capacite),..]
#		indice de l'arete consideree dans cette liste
#		liste des aretes entrante du meme noeud de la forme [(flot, capacite),..]
#		indice de l'arete consideree dans cette liste
#		noeudSortant de la forme (flot, capacite)
#sortie : nouvellevaleur de l'arete

#prendre tout et redonner tout en remplissant les premieres aretes
def ftcArete1(temps, noeudEntrant, aretesParalellesSortantes, indice1, aretesParallesEntrantes, indice2, noeudSortant):
	arete = aretesParalellesSortantes[indice1] # = aussi aretesParallesEntrantes[indice2]
	res = getFlot(arete)
	#L'arete verifie que ses voisines sont pleines, puis prendre tout ce qu'il reste ou tout ce qu'elle peut
	somme1 = 0
	for i in range(indice1):
		somme1 += getCapacite(aretesParalellesSortantes[i]) - getFlot(aretesParalellesSortantes[i])
	res += min(getFlot(noeudEntrant)-somme1, getCapacite(arete) - getFlot(arete))
	
	#L'arete verifie que ses voisines se sont toutes videes, puis se vide tout ce que le noeud sortant peut ou tout ce qu'elle peut
	#Si le noeud sortant peut prendre tout le flot de l'arete, il le fait
	somme2 = 0
	for i in range(indice2):
		somme2 += getFlot(aretesParallesEntrantes[i])
	res -= max(0, min (getCapacite(noeudSortant) - getFlot(noeudSortant) - somme2, getFlot(arete))) #max pour ne pas passer sous 0, min pour prendre le plus petit entre flot de l'arete et capacite restante du noeud
	
	return res
	
#prendre des aretes equitablement et redonner equitablement
def fctArete2(temps, noeudEntrant, aretesParalellesSortantes, indice1, aretesParallesEntrantes, indice2, noeudSortant):
	arete = aretesParalellesSortantes[indice1] # = aussi aretesParallesEntrantes[indice2]
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

	
#TESTS
# print(fctNoeuds1(0, 0, [(1,1),(2,2),(3,3)], (5,6), [(0,4)])) #2
# print(fctNoeuds1(0, 0, [], (5,6), [(0,4)])) #1
# print(fctNoeuds1(0, 0, [], (5,6), [(0,4), (0,1)])) #0
# print(fctNoeuds1(0, 0, [], (5,6), [(0,4), (0,1), (0,1)])) #0
# print(fctNoeuds1(0, 0, [], (5,6), [])) #5
# print(fctNoeuds1(0, 0, [(2,2)], (5,6), [])) #6
# print(fctNoeuds1(0, 0, [(0,2)], (2,30), [(0,2), (0,2)])) #6
# print(fctNoeuds2(0, 0, [(1,1),(2,2),(3,3)], (5,6), [(0,2),(0,2)])) 

# print(ftcArete1(0, (10,10), [(0,6), (0,6)], 1, [(0,6)], 0, (0,5))) # 10-6 = 4
# print(ftcArete1(0, (5,10), [(6,20), (0,7)], 0, [(2,8), (6,20)], 1, (0,5))) # 6+5-(5-2) = 8
# print(ftcArete1(0, (10,10), [(5,6), (1,6), (4,20), (1,1)], 2, [(1,6), (3,4), (0,20), (1,1)], 2, (5,10))) # 4 + (10-(6-5)-(6-1)) - (10-5-(1+3)) = 4 + 4 - 1 = 7
# print(ftcArete1(0, (10,10), [(5,6), (1,6), (4,6 ), (1,1)], 2, [(1,6), (3,4), (0,20), (1,1)], 2, (5,10))) # min(6,4 + (10-(6-5)-(6-1))) - (10-5-(1+3)) = min(6, 4 + 4) - 1 = 5

# print(fctArete2(0, (199,200), [(0,30), (0,120), (10,100), (0,20)], 2, [(0,100)], 0, (0,50))) #0+30, 0+75, 10+74, 0+20
# print(fctArete2(0, (400,400), [(0,30), (0,120), (10,100), (0,20)], 2, [(0,100)], 0, (0,50))) #0+30, 0+120, 10+100, 0+20

# print(fctArete2(0, (0,0), [(50,50)], 0, [(50,100), (50,50),(20,20)], 1, (10,110))) # 10,10,0
# print(fctArete2(0, (0,0), [(50,50)], 0, [(50,100), (50,50),(20,20)], 1, (0,1000))) # 0,0,0

# print(fctArete2(0, (0,0), [(50,80)], 0, [(50,80), (40,100), (100,200), (20,40)], 0, (10,210))) # 0,0,10,0
# print(fctArete2(0, (0,0), [(40,100)], 0, [(50,80), (40,100), (100,200), (20,40)], 1, (10,210))) # 0,0,10,0
# print(fctArete2(0, (0,0), [(100,200)], 0, [(50,80), (40,100), (100,200), (20,40)], 2, (10,210))) # 0,0,10,0
# print(fctArete2(0, (0,0), [(20,40)], 0, [(50,80), (40,100), (100,200), (20,40)], 3, (10,210))) # 0,0,10,0

"""
#Cas ou flot entrant est reparti partiellement et noeud sortant rempli partiellement
print(fctArete2(0, (1000,1000), [(50,80), (40,100), (100,200), (20,40)], 0, [(50,80), (40,100), (100,200), (20,40)], 0, (10,2000)))
print(fctArete2(0, (1000,1000), [(50,80), (40,100), (100,200), (20,40)], 1, [(50,80), (40,100), (100,200), (20,40)], 1, (10,2000)))
print(fctArete2(0, (1000,1000), [(50,80), (40,100), (100,200), (20,40)], 2, [(50,80), (40,100), (100,200), (20,40)], 2, (10,2000)))
print(fctArete2(0, (1000,1000), [(50,80), (40,100), (100,200), (20,40)], 3, [(50,80), (40,100), (100,200), (20,40)], 3, (10,2000))) # Apres prendre : 50+30, 40+60, 100+100, 20+20 #Apres donner : 50-50, 40-40, 100-100, 20-20
#resultat final : 30, 60, 100, 20

print()
#Cas ou flot entrant est reparti entierement et noeud sortant rempli partiellement
print(fctArete2(0, (100,100), [(50,80), (40,100), (100,200), (20,40)], 0, [(50,80), (40,100), (100,200), (20,40)], 0, (10,2000)))
print(fctArete2(0, (100,100), [(50,80), (40,100), (100,200), (20,40)], 1, [(50,80), (40,100), (100,200), (20,40)], 1, (10,2000)))
print(fctArete2(0, (100,100), [(50,80), (40,100), (100,200), (20,40)], 2, [(50,80), (40,100), (100,200), (20,40)], 2, (10,2000)))
print(fctArete2(0, (100,100), [(50,80), (40,100), (100,200), (20,40)], 3, [(50,80), (40,100), (100,200), (20,40)], 3, (10,2000))) # Apres prendre : 50+27, 40+27, 100+26, 20+20 #Apres donner : 50-50, 40-40, 100-100, 20-20
#resultat final : 27, 27, 26, 20

print()
#Cas ou flot entrant est reparti partiellement et noeud sortant rempli entierement
print(fctArete2(0, (1000,1000), [(50,80), (40,100), (100,200), (20,40)], 0, [(50,80), (40,100), (100,200), (20,40)], 0, (10,161)))
print(fctArete2(0, (1000,1000), [(50,80), (40,100), (100,200), (20,40)], 1, [(50,80), (40,100), (100,200), (20,40)], 1, (10,161)))
print(fctArete2(0, (1000,1000), [(50,80), (40,100), (100,200), (20,40)], 2, [(50,80), (40,100), (100,200), (20,40)], 2, (10,161)))
print(fctArete2(0, (1000,1000), [(50,80), (40,100), (100,200), (20,40)], 3, [(50,80), (40,100), (100,200), (20,40)], 3, (10,161))) # Apres prendre : 50+30, 40+60, 100+100, 20+20 #Apres donner : 50-46, 40-40, 100-45, 20-20
#resultat final : 34, 60, 155, 20

print()
#Cas ou flot entrant est reparti entierement et noeud sortant rempli entierement
print(fctArete2(0, (100,100), [(50,80), (40,100), (100,200), (20,40)], 0, [(50,80), (40,100), (100,200), (20,40)], 0, (10,210)))
print(fctArete2(0, (100,100), [(50,80), (40,100), (100,200), (20,40)], 1, [(50,80), (40,100), (100,200), (20,40)], 1, (10,210)))
print(fctArete2(0, (100,100), [(50,80), (40,100), (100,200), (20,40)], 2, [(50,80), (40,100), (100,200), (20,40)], 2, (10,210)))
print(fctArete2(0, (100,100), [(50,80), (40,100), (100,200), (20,40)], 3, [(50,80), (40,100), (100,200), (20,40)], 3, (10,210))) # Apres prendre : 50+27, 40+27, 100+26, 20+20 #Apres donner : 50-50, 40-40, 100-90, 20-20
#resultat final : 27, 27, 36, 20
"""
