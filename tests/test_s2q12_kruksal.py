#from os import chdir
#chdir(r"C:/Users/auran/OneDrive/Documents/ensae/1A/Projet de programmation/projet programmation_dernier essai/ensae-prog23/delivery_network")

import sys 
sys.path.append(r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\delivery_network")

import unittest
from graph import Graph, graph_from_file
from main import kruksal

class Test_GraphLoading(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file(r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.00.in")
        self.assertEqual(kruksal(g), frozenset(g) )
    
if __name__ == '__main__':
    unittest.main()