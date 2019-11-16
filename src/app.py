import math

from itertools import permutations
from itertools import combinations

DATA_5_CLIENT_PATH = "./tai5.dat"
DATA_10_CLIENT_PATH = "./tai10.dat"

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
dados = []
problema = extract_from_data_file(DATA_10_CLIENT_PATH)

clientes = []
for i in range(0, len(problema["dados"])):
    clientes.append(problema["dados"][i][0])

cliente_perm = permutations(clientes)

rotas = init_routes(problema["qtd_cliente"] - 1)
max_num_of_routes = len([*rotas])

for num_rotas in range(
    3, max_num_of_routes + 2
):  # este for explora as quantas rotas vai ter minha solução
    sets_of_routes_combinations = combinations([*rotas], num_rotas - 1)
    for set_of_routes in list(sets_of_routes_combinations):  # faz todas as possibilidades de rotas de tamanho NUM_ROTA
        # print(i) # onde vai ser o corte
        for route_endpoint in set_of_routes:
            rotas[route_endpoint] = True # Adiciona True nos cortes das rotas
        # print(rotas) # como ficou o corte
        solucao = [] # Zera a solução
        route = [] # Zera a rota

        for client_point in list(cliente_perm):  # permutacao dos clientes
            print(client_point)
            route.append(client_point[0]) # O primeiro ponto de parada sempre entra na rota
            for route_index in range(0, max_num_of_routes):  # constrói a solução
                if rotas[route_index] is True:
                    solucao.append(route)
                    route = [] # Zera a rota
                route.append(client_point[route_index + 1])
            solucao.append(route)
            print(solucao, "\n")

            # for teste in client_point:
            #   print(problema['dados'][teste-1])

            solucao = [] # Zera a solução
            route = [] # Zera a rota

        rotas = init_routes(problema["qtd_cliente"] - 1) # Inicializa as rotas para as novas combinações de rotas

