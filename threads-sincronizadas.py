from multiprocessing import Process, Value
from random import *
from time import *
from threading import Thread

def sleeping(name, shared_x):
    s=randint(1,3)

    t=localtime()
    txt=str(t.tm_min)+':'+str(t.tm_sec)+' '+ name +' is going to sleep for '+str(s)+' seconds'
    print(txt)

    sleep(s)

    t=localtime()

    with shared_x.get_lock():
        shared_x.value += 1

    txt=str(t.tm_min)+':'+str(t.tm_sec)+' '+name+' has woken up, seeing shared_x being '+ str(shared_x)
    print(txt)

def sleeper(name, shared_x):
    sleeplist=list()
    for i in range(3):
        subsleeper=Thread(target=sleeping,args=(name+' '+str(i),shared_x))
        sleeplist.append(subsleeper)
    for s in sleeplist:s.start()
    for s in sleeplist:s.join()

if __name__ == "__main__":
    shared_x = Value('i', randint(10,99)) 
    p=Process(target=sleeper,args=('eve',shared_x))
    q=Process(target=sleeper,args=('bob',shared_x))
    p.start();q.start()
    p.join();q.join()