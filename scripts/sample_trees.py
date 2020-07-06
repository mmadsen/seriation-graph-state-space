#!/usr/bin/env python
import ray
import time
import networkx as nx
import matplotlib.pyplot as plt


@ray.remote
def processor_task(work_item):
	g = nx.generators.trees.random_tree(20)
	evals = nx.laplacian_spectrum(g).tolist()
	return evals 



if __name__ == "__main__":
	ray.init(webui_host='0.0.0.0')


	for i in range(1000):
		with open(f"/data/experiments/tree-spectra/random_tree_spectra_{i}.csv", 'w') as f:
			print(f"Starting batch {i} of 10MM graphs...")
			for i in range(10000):
				futures = [processor_task.remote(s) for s in range(100)]
				while len(futures) > 0:
					finished, rest = ray.wait(futures, timeout=1)

					for id in finished:
						res_list = ray.get(id)
						f.write(",".join(map(str, res_list)))
						f.write("\n")
					futures = rest
