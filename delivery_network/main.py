from graph import Graph, graph_from_file

'''
data_path = "input/"
file_name = "network.01.in"

g = graph_from_file(data_path + file_name)
print(g)
'''
#Séance 2  
import sys 
sys.path.append("delivery_network")

def duration(file,N):
    g= graph_from_file(file)
    n=g.nb_nodes
    D=[]
    for k in range (N):
        src,dest=random.randrange(n), random.randrange(n)
        start=time.perf_counter()
        g.min_power(src,dest)
        stop=time.perf_counter()
        D.append(stop-start)
    return D

print(duration(r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23-1\ensae-prog23\input\routes.2.in", 5))

