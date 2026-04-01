from multiprocessing import Process
from time import *
from random import *

def sleeper(name): # função que representa a tarefa a ser executada
    s=randint(1,20)
    t=localtime()
    txt=str(t.tm_hour)+':'+str(t.tm_min)+':'+str(t.tm_sec)+' '+ name +' is going to sleep for '+str(s)+' seconds'
    print(txt)
    sleep(s)
    t=localtime()
    txt=str(t.tm_hour)+':'+str(t.tm_min)+':'+str(t.tm_sec)+' '+ name +' has woken up'
    print(txt)

if __name__ == "__main__":
    p=Process(target=sleeper,args=('eve',))
    q=Process(target=sleeper,args=('bob',))
    p.start();q.start()
    p.join();q.join()