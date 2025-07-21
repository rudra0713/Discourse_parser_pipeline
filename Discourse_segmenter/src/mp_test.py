from multiprocessing import Process, Queue
import random

arr = [1,2,3,4,5,6,7,8]


def rand_num(start_index):
    end_index = start_index + 2
    t = {}
    print("end : ", end_index)
    for a in arr[start_index: end_index]:
        t.update({a: a*2})
    queue.put(t)


if __name__ == "__main__":
    queue = Queue()

    processes = [Process(target=rand_num, args=(x, )) for x in range(0, len(arr), 2)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    results = {}
    for _ in processes:
        results.update(queue.get())
    # results = [queue.get() for p in processes]

    print(results)
