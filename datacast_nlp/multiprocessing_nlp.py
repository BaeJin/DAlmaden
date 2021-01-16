from multiprocessing import Pool, TimeoutError,Process,cpu_count
from datacast_nlp.db_nlp import run_nlp
import os

def main():
    process_list = []
    available_cpu = cpu_count()
    for i in range(0, 6):
        print(available_cpu)
        process = Process(target=run_nlp,args=(str(i),))
        process_list.append(process)
    for process in process_list:
        process.start()

if __name__ =='__main__':
    main()