import ray
import asyncio
import numpy as np
import time


ray.init(webui_host='0.0.0.0')

samples = np.random.uniform(1,60,10)
print(samples)
# @ray.remote
# def calculate(record):
# 	time.sleep(record)
# 	return record





# futures = [calculate.remote(s) for s in samples]

# while len(futures) > 0:
# 	finished, rest = ray.wait(futures)
# 	value = ray.get(finished[0])
# 	print(f"Completed task - value: {value}")
# 	futures = rest		


@ray.remote
class AlgorithmWorker:
	async def process(self, work_item):
		await asyncio.sleep(work_item)
		print(f"... Woke after {work_item} seconds sleeping")
		return work_item

worker = AlgorithmWorker.remote()

@ray.remote
def processor_task(work_item):
	time.sleep(work_item)
	print(f"... Woke after {work_item} seconds sleeping")
	return work_item




async def main():
	futures = [processor_task.remote(s) for s in samples]
	print(futures)
	while len(futures) > 0:
		finished, rest = ray.wait(futures, timeout=1)
		print(f"Incomplete: {len(rest)}")
		futures = rest



asyncio.get_event_loop().run_until_complete(main())
