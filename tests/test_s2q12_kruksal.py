import sys 
sys.path.append(r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\delivery_network")

import unittest
from graph import Graph, graph_from_file
from main import kruskal

class Test_GraphLoading(unittest.TestCase):
    def test_network03(self):
        g=graph_from_file(r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.03.in")
        g_expected={1:[(2,10,1)],
                    2:[(1,10,1),(3,4,1)],
                    3:[(2,4,1),(4,4,1)],
                    4:[(3,4,1)],
                    }
        self.assertEqual(kruskal(g),g_expected)

    def test_network04(self):
        g=graph_from_file(r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\projet programmation_dernier essai\ensae-prog23\input\network.04.in")
        g_expected={1:[(2,4,89)],
                    2:[(1,4,89),(3,4,3)],
                    3:[(2,4,3),(4,4,2)],
                    4:[(3,4,2)]
                    }
        self.assertEqual(kruskal(g),g_expected)

if __name__ == '__main__':
    unittest.main()