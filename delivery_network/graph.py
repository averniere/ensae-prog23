class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
    
    #On veut trouver s'il existe un chemin que le camion puisse parcourir avec sa puissance power et s'il 
#existe quel est ce chemin. Pour ce, on construit une sous fonction renvoyant le chemin, s'il existe,
#entre un noeud et la destination. 

    def get_path_with_power(self, src, dest, power):
        verif={node:False for node in self.nodes} #dictionnaire indiquant les noeuds visit??s ou non, 
        #afin d'??viter, par exemple de faire des aller-retours entre deux noeuds.
        verif[src]=True
        def path(node, chemin):
            if node==dest:  #condition d'arr??t: si l'on est arriv?? ?? destination, on retourne le chemin
                return chemin
            list_nghbr=self.graph[node]
            for voisin in list_nghbr:   #on parcourt les voisins du noeud
                nghbr=voisin[0]
                if voisin[1]<=power and not verif[nghbr]: #si le camion a une puissance suffisante pour
                    #traverser l'ar??te et que le voisin n'a pas d??j?? ??t?? visit??
                    verif[nghbr]=True
                    chemin.append(nghbr)    #on ajoute le voisin au chemin car il convient
                    return path(nghbr,chemin)   #on r??applique la fonction ?? ce nouveau noeud sur lequel
                #le camion se trouve
                if voisin==self.graph[node] and chemin[-1]!=src:    #condition si jamais le camion arrive
                    #dans un cul-de-sac
                    verif[nghbr]=True
                    chemin.pop()
                    return path(chemin[-1],chemin)
            return None
        return path(src,[src])

    '''
Analyse de la complexit?? de get_path_with power:
On note n le nombre de noeuds du graphe et m le nombre de cul-de-sacs. 
A chaque fois que l'on tombe dans une impasse, ie un noeud qui n'a pas d'autre voisin que celui d'o?? 
le camion vient, le camion doit retourner en arri??re et reparcourir les voisins du noeud pr??c??dent, 
jusqu'?? trouver, ou non, un nouveau chemin par o?? passer. On peut majorer le nombre de fois o?? l'on 
effectue les op??rations de la boucle for (nombre d'op??rations born??, donc en O(1) ?? chaque it??ration) 
par n*m. D'o?? une complexit?? en O(n*m).
    '''
    
#D??termination des composantes connexes d'un graphe:
#On ??crit une fonction r??cursive permettant de d??terminer la composante connexe dans laquelle se trouve 
#un noeud: tant qu'un noeud a des voisins et que ces derniers n'ont pas ??t?? visit??s, on les ajoute ??
#la composante connexe et l'on r??effectue la fonction sur chacun d'eux. La fonction s'arr??te lorsque
#tous les noeuds ont ??t?? visit??s. 
    

    def connected_components(self):
        connected_components=[]
        vnodes={node:False for node in self.nodes}  #marqueur pour savoir si un noeud a d??j?? ??t?? visit??
        
        def component(node):
            C=[node]    #liste repr??sentant une composante connexe
            for list_nghbr in self.graph[node]:
                nghbr=list_nghbr[0]
                if not vnodes[nghbr]:
                    vnodes[nghbr]=True
                    C+=component(nghbr)
            return C
        
        for node in self.nodes:
            if not vnodes[node]:
                connected_components.append(component(node))
        return connected_components


    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    #On d??termine la puissance minimale n??cessaire pour effectuer un trajet par recherche dichotomique:
#on utilise pour ce, la fonction get_path_with_power qui d??termine si un camion avec une certaine 
#puissance peut effectuer un certain trajet et renvoie le chemin si c'est le cas. L'id??e est de trouver
#un intervalle de puissances de d??part, pour une partie desquelles le camion peut effectuer le trajet
#voulu, et de r??duire cet intervalle en le divisant successivement par deux, jusqu'?? approcher la 
#puissance minimale recherch??e.

    def min_power(self, src, dest):
        g=0
        d=1
        eps=10**(-3)
        def rechdicho(g,d): #fonction de recherhce dichotomique de la puissance
            while abs(g-d)>eps:
                m=(d+g)/2
                if self.get_path_with_power(src,dest,m)!=None:
                    d=m
                else:
                    g=m
                rechdicho(g,d)
            if d-int(d)<0.5:    #on conditionne pour renvoyer un entier et non un flottant
                return self.get_path_with_power(src,dest,d),int(d)
            else:  
                return self.get_path_with_power(src,dest,d),int(d)+1
        while self.get_path_with_power(src, dest, d)==None: #condition n??cessaire si au d??but une 
            #puissance inf??rieure ?? 1 ne suffit pas pour effectuer le trajet voulu
            g=d
            d=10*d
        return rechdicho(g,d)
        
    '''
Complexit?? de l'algorithme:
D??terminons d'abord la complexit?? de la fonction de recherche dichotomique. Etant donn?? que l'on divise 
?? chaque fois par deux la taille de l'intervalle, originalement de taille d-g, jusqu'?? obtenir une 
longueur d'intervalle inf??rieure ?? eps, le nombre total d'it??ration N effectu?? v??rifie:
N=E(log2((d-g)/eps)) +1 o?? E d??signe la partie enti??re
D'o?? une complexit?? en O(log2((d-g)/eps))
On note ?? pr??sent p la puissance maximale existante sur le graphe. 
Dans le pire des cas, l'on doit passer par l'ar??te de puissance p. Si p>1 on doit parcourir la boucle
while de la fin du code E(log10(p))+1 fois, soit un co??t de O(log10(p)).
On conna??t la complexit?? de get_path_with_power appel??e environ log10(p) fois dans min_power.
    '''

def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    g: Graph
        An object of the class Graph with the graph from file_name.
    """
    '''
    file = open(filename,'r', encoding="utf-8")
    lines = file.readlines()
    file.close()
    g=Graph([i for i in range(1, int(lines.pop(0).split()[0])+1)])
    for line in lines:
        words= line.split()
        if len(words)==3:
            g.add_edge(int(words[0]), int(words[1]), int(words[2]))
        else:
            g.add_edge(int(words[0]), int(words[1]), int(words[2]), int(words[3]))
    return(g)
    '''
    with open(filename, "r") as file:
        L=list(map(int, file.readline().split()))
        if len(L)==2:
            n, m = L
            g = Graph(range(1, n+1))
        elif len(L)==1:
            m=L[0]
            g= Graph(range(1,m+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g
