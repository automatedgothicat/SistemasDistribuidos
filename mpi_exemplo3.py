# mpiexec -n 8 python mpi_exemplo3.py
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size < 2:
    raise SystemExit("Execute com pelo menos 2 processos")

dest = (rank + 1) % size
src  = (rank - 1) % size

comm.send(f"Mensagem do {rank}", dest=dest)
msg = comm.recv(source=src)
print(f"[{rank}] recebeu: {msg}")