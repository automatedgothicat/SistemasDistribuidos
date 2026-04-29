
# Exemplo: Envio e Recebimento de Mensagem com MPI
# criando comunicador e obtendo o rank de um processo

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
num = comm.Get_size()
print('My rank is ',rank)
print('Numero de processos: ',num)
