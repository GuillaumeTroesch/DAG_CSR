from CSR import *

isDAGFormat = False

#Recupère la valeur de chaque noeud du fichier fourni
def getListValeurNoeud(listnoeud, linenodesvalue):
    listValeurNoeud = []
    for i in listnoeud:
        listValeurNoeud.append((0,int(linenodesvalue[int(i)].split("\n")[0])))
    return listValeurNoeud

#Initialise la liste utilisee pour creer le CSR et la liste des parents des sommets/aretes
def initListsSommet(linefichiervalnoeud):
    listVoisinsSommet = []
    listIndexParentEdge = []
    compteurNumSommet = 0
    for line in linefichiervalnoeud:
        listVoisinsSommet.append((str(compteurNumSommet), [], 0, []))
        listIndexParentEdge.append([])
        compteurNumSommet += 1
    return listVoisinsSommet, listIndexParentEdge

def readFileDot(filedot, fileegdesvalue, filenodesvalue):
    lines = open(filedot, "r").readlines()

    linesValNoeuds = []
    linesValAretes = []
    global isDAGFormat
    if fileegdesvalue != "" and filenodesvalue != "":
        isDAGFormat = True
        linesValAretes = open(fileegdesvalue, "r").readlines()
        linesValNoeuds = open(filenodesvalue, "r").readlines()

    #liste de tuples avec le format (sommet, [liste sommets voisins], nombreVoisins, [listeValAretes])
    listVoisinsSommet = []
    listIndexParentEdge = []
    fileNodeIndex = 0

    if isDAGFormat:
        listVoisinsSommet, listIndexParentEdge = initListsSommet(linesValNoeuds)

    compteurLineEdge = 0
    
    #Lit les voisins de chaque noeuds pour récupérer les infos nécéssaires à la création du CSR
    for line in lines:
        if "->" in line:
            sommet1 = None
            sommet2 = None
            labelArete = None

            if isDAGFormat:
                (sommet1, _, sommet2, _, _, _) = line.split()
            if not isDAGFormat:
                (sommet1, _, sommet2, labelArete) = line.split()

            listIndexParentEdge[int(sommet2)].append(compteurLineEdge)

            #Ajoute les informations à listVoisinsSommets
            for i in range(0, len(listVoisinsSommet)):
                (s, listS, nombreSommets, listValAretes) = listVoisinsSommet[i]
                if sommet1 == s:
                    listS.append(sommet2)

                    #On récupère la liste des valeurs des arêtes en fonction du format
                    if isDAGFormat:
                        listValAretes.append(int(linesValAretes[fileNodeIndex].split("\n")[0]))
                        # Incrémente l'index de la liste du fichier des valeurs des noeuds pour le parcourir
                        fileNodeIndex += 1
                    else:
                        listValAretes.append(int(extractLabel(labelArete).split("/")[1].split('"')[0]))

                    listVoisinsSommet[i] = (s, listS, nombreSommets+1, listValAretes)
                    break
            compteurLineEdge += 1

    return genCSR(listVoisinsSommet, linesValNoeuds, listIndexParentEdge)

#Renvoie le CSR à partir de la liste de tuples récupérée fournie par readFileDot(...)
def genCSR(listetuplesommet, linenodesvalue,listindexparentedge):

    listNoeuds = []
    listValeursNoeuds = []
    listAreteCount = [0]
    listVoisins = []
    listValeursArete = []

    #Rempli les tableaux du CSR
    countSommets = 0
    for (nomSommet, voisins, nombreVoisins, valeurAretes) in listetuplesommet:
        #Liste noeuds
        listNoeuds.append(nomSommet)
        #Liste CSR 1
        countSommets += nombreVoisins
        listAreteCount.append(countSommets)
        #Liste CSR 2
        for voisin in voisins:
            listVoisins.append(int(voisin))
        #liste valeurs aretes
        for valArete in valeurAretes:
            va = (0, valArete)
            listValeursArete.append(va)

    if isDAGFormat:
        #Liste des valeurs des noeuds
        listValeursNoeuds = getListValeurNoeud(listNoeuds, linenodesvalue)

    #TODO listindexparentedge a ete supprimee, il fut la supprimer totalement
    return CSR(listNoeuds, listValeursNoeuds, listAreteCount, listVoisins, listValeursArete)

#Recupère le tuple (numNoeud, label)
def getNoeudsGraph(dotgraph):
    listNode = []
    for line in dotgraph:
        if ("{" not in line) and ("}" not in line) and ("->" not in line):
            [numNoeud, labelNoeud] = line.split()  # On suppose nomNoeud est un int
            exctractedLabelNoeud = extractLabel(labelNoeud)
            listNode.append((numNoeud, exctractedLabelNoeud))
    return listNode

#Recupère le label d'un noeud ou d'un sommet
def extractLabel(strlabel):
    return strlabel.split("=")[1].split("]")[0]

# Export d'un csr vers un fichier .dot
def exportFileDot(csr, filename):
    fichier = open(filename, "w")
    fichier.write("digraph CSR {\n")

    # Ecriture des sommets
    listValeurNoeuds = csr.getValeurNoeuds()
    for i in range(0, len(listValeurNoeuds)):
        (flot, flotMax) = listValeurNoeuds[i]
        fichier.write(str(i) + ' [label="' + str(i) +"\\n"+ str(flot) + "/" + str(flotMax) + '"]\n')

    # Ecriture des aretes
    for idArete in range(csr.getNbAretes()):
        fichier.write(str(csr.getNoeudEntrantArete(idArete)) + " -> " + str(csr.getNoeudSortantArete(idArete)) + '[label="'+str(idArete) +"\\n"+ str(csr.getValeurArete(idArete)) + '"]\n')

    fichier.write("}")
    fichier.close()
