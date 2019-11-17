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
        'origin': [0, int(datContent[2][0]), int(datContent[2][1])],
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

def calc_route(route, route_data, origin):
    distance = 0
    p1 = {}
    p2 = {}
    routes_info = [r for r in route_data if r[0] in route]
    routes_info.append(origin)
    number_of_routes_points = len(routes_info)
    for i in range(0,number_of_routes_points):
        p1 = {'x': routes_info[i][1],'y':routes_info[i][2]}
        if(i == number_of_routes_points - 1):
            p2 = {'x': routes_info[0][1],'y':routes_info[0][2]}
        else:
            p2 = {'x': routes_info[i+1][1],'y':routes_info[i+1][2]}
        distance += get_distance(p1,p2)
    return distance

def calc_set_of_routes_coast(routes, routes_data, origin):
    coast = 0
    for route in routes:
        coast += calc_route(route, routes_data, origin)
    return coast

def is_over_weight(route, route_data, max):
    route_coast = 0
    routes_info = [r for r in route_data if r[0] in route]
    for route in routes_info:
        route_coast += route[3]
    if route_coast > max:
        return True
    return False

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

cliente_perm = list(permutations(clientes))

rotas = init_routes(problema["qtd_cliente"] - 1)
max_num_of_routes = len([*rotas])

for num_rotas in range(
    3, max_num_of_routes + 2
):  # este for explora as quantas rotas vai ter minha solução
    sets_of_routes_combinations = list(combinations([*rotas], num_rotas - 1))
    for set_of_routes in sets_of_routes_combinations:  # faz todas as possibilidades de rotas de tamanho NUM_ROTA
        # print(i) # onde vai ser o corte
        print(set_of_routes)
        for route_endpoint in set_of_routes:
            rotas[route_endpoint] = True # Adiciona True nos cortes das rotas
        # print(rotas) # como ficou o corte
        solucao = [] # Zera a solução
        route = [] # Zera a rota
        bad_solution = False
        for clients_points in cliente_perm:  # permutacao dos clientes
            route.append(clients_points[0]) # O primeiro ponto de parada sempre entra na rota
            for route_index in range(0, max_num_of_routes):  # constrói a solução
                if rotas[route_index] is True:
                    check_route = is_over_weight(route, problema['dados'], problema['capacidade'])
                    if not check_route:
                        solucao.append(route)
                        route = [] # Zera a rota
                    else:
                        bad_solution = True
                        break
                route.append(clients_points[route_index + 1])
            check_route = is_over_weight(route, problema['dados'], problema['capacidade'])
            if not check_route and not bad_solution:
                solucao.append(route)
                set_of_routes_coast = calc_set_of_routes_coast(solucao, problema['dados'], problema['origin'])
                dados.append({'solucao':solucao, 'coast': set_of_routes_coast})
                print("=============== // =================")
                print(f"Solução: {solucao}")
                print(f"Custo: {set_of_routes_coast}")
                print("=====================//==================")

            # for teste in client_point:
            #   print(problema['dados'][teste-1])

            solucao = [] # Zera a solução
            route = [] # Zera a rota

        rotas = init_routes(problema["qtd_cliente"] - 1) # Inicializa as rotas para as novas combinações de rotas

best_solution = {'solution': [], 'coast': 10000}
coasts = []
for data in dados:
    coasts.append(int(data['coast']))
    if data['coast'] < best_solution['coast']:
        best_solution['coast'] = data['coast']
        best_solution['solution'] = data['solucao']

    print('solucao:',data['solucao'])
    print('coast:',data['coast'])

print(f"Best solution: {best_solution['solution']}")
print(f"Coast of solution: {best_solution['coast']}")
print("Coast should be:", min(coasts))
