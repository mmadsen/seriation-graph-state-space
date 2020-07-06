#!/usr/bin/env python
import ray
import time
import networkx as nx
import matplotlib.pyplot as plt


@ray.remote
def processor_task(work_item):
    eigen_list = []
    for _ in range(10):
        g = nx.generators.trees.random_tree(20)
        evals = nx.laplacian_spectrum(g)
        eigen_list.append(list(evals))
    return eigen_list



if __name__ == "__main__":
    ray.init(webui_host='0.0.0.0', address="127.0.0.1:9999")

    with open("random_tree_spectra.csv", 'w') as f:
        futures = [processor_task.remote(s) for _ in range(10)]
        print(futures)
        while len(futures) > 0:
            finished, rest = ray.wait(futures, timeout=1)
            for id in futures:
                res_list = ray.get(id)
                for row in res_list:
                    f.write(",".join(row))
            print(f"Incomplete: {len(rest)}")
            futures = rest
