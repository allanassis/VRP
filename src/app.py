import math

from itertools import permutations
from itertools import combinations

DATA_5_CLIENT_PATH = "./tai5.dat"
DATA_10_CLIENT_PATH = "./tai10.dat"

def criar_solucao():
    solucao = []
    return solucao


def zerar_temp():
    temp = []
    return temp


def extract_from_data_file(file_path):
    datContent = [i.strip().split() for i in open(file_path).readlines()]
    vrp_info = {
        "qtd_cliente": int(datContent[0][0]),
        "capacidade": int(datContent[1][0]),
        "dados": [],
    }
    for i in range(3, len(datContent)):
        datContent[i] = list(
            map(int, datContent[i])
        )  # converte o conteudo de str pra int
        vrp_info["dados"].append(datContent[i])
    return vrp_info


def get_distance(p1, p2):
    dist = math.sqrt((p2["x"] - p1["x"]) ** 2 + (p2["y"] - p1["y"]) ** 2)
    return dist


def init_routes(qnt):
    routes = { i: False for i in range(0, qnt) }
    return routes


###################
# FIM DAS FUNCOES #
###################

melhor = 0
distancia = 0
dados = []  # estrutura que sera adicionada ao dicionario
problema = extract_from_data_file(DATA_10_CLIENT_PATH)

clientes = []  # estrutura que sera permutada
# criando o array de clientes
for i in range(0, len(problema["dados"])):
    clientes.append(problema["dados"][i][0])

rotas = init_routes(problema["qtd_cliente"] - 1)
max_num_of_routes = len([*rotas])

for num_rotas in range(
    3, max_num_of_routes + 2
):  # este for explora as quantas rotas vai ter minha solução
    y = combinations([*rotas], num_rotas - 1)
    for i in list(y):  # faz todas as possibilidades de rotas de tamanho NUM_ROTA
        # print(i) # onde vai ser o corte
        for j in i:  # marca com o numero 1 os cortes
            rotas[j] = True
        # print(rotas_corte) # como ficou o corte

        solucao = criar_solucao()
        temp = zerar_temp()

        cliente_perm = permutations(clientes)
        for caso_cliente in list(cliente_perm):  # permutacao dos clientes
            print(caso_cliente)  # qual permutacao esta sendo trabalhada
            temp.append(caso_cliente[0])
            for k in range(0, max_num_of_routes):  # constrói a solução
                if rotas[k] is True:
                    solucao.append(temp)
                    temp = zerar_temp()
                temp.append(caso_cliente[k + 1])
            solucao.append(temp)
            print(solucao, "\n")

            # for teste in caso_cliente:
            #   print(problema['dados'][teste-1])

            solucao = criar_solucao()
            temp = zerar_temp()

        rotas = init_routes(problema["qtd_cliente"] - 1)

