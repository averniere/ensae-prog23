from graph import Graph, graph_from_file
import time
import random
import copy

'''
data_path = "input/"
file_name = "network.01.in"

g = graph_from_file(data_path + file_name)
print(g)
'''


#Séance 2  

'''
On implémente une fonction permettant d'évaluer un temps moyens un graphe
'''
def duration(filename, src, dest):
    g= graph_from_file(filename)
    start=time.perf_counter()
    g.min_power(src,dest)
    stop=time.perf_counter()
    return(stop-start)      

def duration_allroute(filename1, filename2,N):
    with open(filename1, "r") as file:
        nb_trajet=list(map(int, file.readline().split()))
        avg_time=0
        for _ in range (N):
            src, dest, cost=list(map(int, file.readline().split()))
            avg_time+=duration(filename2, src, dest)/N
            print(avg_time)
        tot_time=nb_trajet*avg_time
    return tot_time


#print(duration_allroute(filename2_1,filename2_2, 5))

'''
Question 12

On définit les fonctions permettant d'appliquer la méthode UnionFind: makeset permettant de créer des 
singletons contenant chaque noeud du graphe, find permettant de trouver quel est le noeud parent (la
racine) d'un noeud et union permettant d'unir deux sous arbres, sans qu'ils ne forment de cycle.
    
'''

def makeset(parent, rank, n): #fonction qui créé initialement n singletons, où n est le nombre de noeuds
    for i in range(1,n+1):
        parent[i]=i
        rank[i]=0

#Fonction permettant de trouver la racine d'un noeud. Si plusieurs noeuds ont la même racine, ils 
#appartiennent au même sous arbre. On choisit pour racine commune de ces noeuds, le noeud le plus en 
#'profondeur' dans le graphe.

def find(parent,k):  
    if parent[k]==k:
        return k
    return find(parent, parent[k])

#Fonction permettant d'unir deux sous-arbres. On attribue à chaque noeud un rang: cela permet de déterminer
#si, lorsque l'on doit unir deux sous arbres, on garde le noeud du premier ou du deuxième sous arbre 
# comme origine de l'arbre résultant. Les noeuds à l'origine des sous arbresont le rang le plus élevé.
# Le rang symbolise donc ici la profondeur d'un noeud dans un arbre.

def union(parent, rank, i,j): 
    root_i=find(parent,i)
    root_j=find(parent,j)
    if root_i!=root_j:
        if root_i<root_j:
            parent[root_i]=root_j
        else:
            parent[root_j]=root_i
            if rank[root_i]==rank[root_j]:
                rank[root_i]+=1

'''On écrit alors les fonctions nécessaires pour renvoyer un arbre couvrant de puissance minimale. 
'''

#Fonction permettant d'obtenir la liste des arêtes par ordre de puissance croissant

def sort_by_power(g):
    L_edges=[]
    list_n=g.nodes
    n=g.nb_nodes
    dico=g.graph
    for node in g.nodes:
        for ngbr in dico[node]:
            l=node, ngbr[0],ngbr[1],ngbr[2]
            if frozenset(l) not in L_edges:
                L_edges.append(l)
    L_sort_by_power=sorted(L_edges,key=lambda x:x[2])
    return L_sort_by_power

#Algorithme inspiré de l'algorithme de Kruskal

def kruskal(g):
    parent={}
    rank={}
    new_g=Graph([])
    makeset(parent, rank, g.nb_nodes)
    g_sorted=sort_by_power(g)
    for k in range (len(g_sorted)):
        n1=g_sorted[k][0]
        n2=g_sorted[k][1]
        if find(parent,n1)!=find(parent,n2):
            new_g.add_edge(n1,n2,g_sorted[k][2])
            union(parent,rank,n1,n2)
    print(new_g)
    return new_g
    
#g0=graph_from_file(r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.03.in")
#print(kruskal(g0))


'''Question 14
On adapte légèrement l'algorithme de parcours en largeur d'un arbre, pour qu'il retourne le trajet entre
deux noeuds d'un sous arbre. On écrit ensuite une fonction retournant la puissance minimale et le chemin 
pour effectuer un trajet entre deux noeuds du sous arbre. 
Etant donné qu'il s'agit d'un sous arbre couvrant de poids minimal, la puissance minimale nécessaire pour
effectuer un trajet entre src et dest, correspond à la puissance maximale que l'on puisse trouver sur le
trajet trouvé. 
'''
def bfs(src,dest,g):
    queue=[(src,[src])] #file d'attente des noeuds à visiter 
    while queue!=[]:
        (node,path)=queue.pop(0) #on supprime le noeud de la file d'attente lorsque l'on parcourt ses voisins
        for ngb in g.graph[node]:
            if ngb[0]==dest:
                path.append(dest)
                return path
            else:
                if ngb[0] not in path:
                    queue.append((ngb[0],path+[ngb[0]]))
    return None

'''
Dans le pire des cas, en effectuant cet algorithme, il est possible de parcourir tous les noeuds du sous-
arbre couvrant. Par ailleurs, il est impossible, lorsque l'on applique cet algorithme à un sous-arbre, de
repasser plusieurs fois par le même noeud. En effet, lorque l'on parcourt les voisins d'un noeud placé
en liste d'attente auparavant, si un voisin a déjà été parcouru, alors il est contenu dans le chemin (path)
associé au noeud dont on s'occupe.
Ainsi, la complexité temporelle de cet algorithme est en O(n), où n est le nombre de noeud du graphe.
'''

def new_min_power(src,dest,g):
    path=bfs(src,dest,g)
    pow=0
    if path!=[]:
        for k in range(len(path)-1):
            node=path[k]
            for ngb in g.graph[node]:
                if ngb[0]==path[k+1] and ngb[1]>pow:
                    pow=ngb[1]
    return path,pow

'''
Complexité de l'algorithme.
Dans le cas où path existe entre src et dest, on note p=len(path), n le nombre de noeuds du graphe.
On parcourt une boucle for de longueur ~p, au sein de laquelle on parcourt une autre boucle for de
longueur égale au nombre de voisins du noeud considéré. 
'''

'''
Question 15
'''
def new_duration(filename1, filename2, src, dest):
    g= graph_from_file(filename1)
    start=time.perf_counter()
    new_g=kruskal(g)
    T,pow=new_min_power(src,dest,new_g)
    stop=time.perf_counter()
    with open(filename2, "a") as file:
        file.write(str(pow)+"\n")
    return(stop-start)      

def new_duration_allroute(filename1, filename2,filename3):
    with open(filename1, "r") as file:
        nb_trajet=list(map(int, file.readline().split()))[0]
        tot_time=0
        for _ in range (nb_trajet):
            src, dest, cost=list(map(int, file.readline().split()))
            tot_time+=new_duration(filename2, filename3, src, dest)
            print(tot_time)
    return tot_time

'''
Temps d'exécution (tot_time) obtenus pour les différents fichiers routes:
route.1=0.3646744997240603

'''
print(new_duration_allroute(filename1_1,filename1_2,filename1_3))

filename1_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.1.in"
filename1_2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.1.in"
filename1_3=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.1.out"

filename2_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.2.in "
filename2_2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.2.in "
filename2_3=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.3.out"

filename3_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.3.in"
filename3_2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.3.in"
filename3_3=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.3.out"

filename4_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.4.in"
filename4_2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.4.in"
filename4_3=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.4.out"

filename5_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.5.in"
filename5_2="C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.5.in"
filename5_3=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.5.out"

filename6_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.6.in"
filename6_2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.6.in"
filename6_3=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.6.out"

filename7_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.7.in"
filename7_2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.7.in"
filename7_3=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.7.out"

filename8_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.8.in"
filename8_2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.8.in"
filename8_3=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.8.out"

filename9_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.9.in"
filename9_2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.9.in"
filename9_3="C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.9.out"

filename10_1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.10.in"
filename10_2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.10.in"
filename10_3=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\routes.10.out"






