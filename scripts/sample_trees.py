#!/usr/bin/env python

import time
import networkx as nx
import matplotlib.pyplot as plt




if __name__ == "__main__":
    for i in range(50):
        g = nx.generators.trees.random_tree(20)
        # nx.draw(g)
        # plt.show()
        evals = nx.laplacian_spectrum(g)
        print(list(evals))
