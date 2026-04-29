from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

meu_numero = (rank + 1) * 7  

soma = comm.reduce(meu_numero, op=MPI.SUM, root=0)
maximo = comm.reduce(meu_numero, op=MPI.MAX, root=0)

if rank == 0:
    print("Reduce SUM:", soma, flush=True)
    print("Reduce MAX:", maximo, flush=True)