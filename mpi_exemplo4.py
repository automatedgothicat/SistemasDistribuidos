from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size < 2:
    raise SystemExit("Execute com pelo menos 2 processos")

data = None
if rank == 0:
    data = "Ola vizinhos!"
data = comm.bcast(data, root=0)
print(f"[{rank}] recebeu: {data}")