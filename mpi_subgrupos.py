from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Divide em 2 grupos: ranks 0-3 e ranks 4-7
color = 0 if rank < 4 else 1
subcomm = comm.Split(color=color, key=rank)

subrank = subcomm.Get_rank()
subsize = subcomm.Get_size()
print(rank, "-> subrank", subrank, "subsize", subsize)