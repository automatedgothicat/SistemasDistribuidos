from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size < 2:
    raise SystemExit("Execute com pelo menos 2 processos")

if rank == 0:
    valores = [10 * i for i in range(size)]  # um valor para cada rank
else:
    valores = None

meu_valor = comm.scatter(valores, root=0)

# cada rank transforma o valor
resultado = meu_valor + rank

# junta tudo no rank 0
todos = comm.gather(resultado, root=0)

if rank == 0:
    print("Valores originais:", valores, flush=True)
    print("Resultados por rank:", todos, flush=True)