import sys
from random import randrange
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# lê o arquivo com os pontos
def readFile(filename):
    header, points = {}, []
    with open(filename) as f:
        # processa o cabeçalho do arquivo
        facilities, range = f.readline().split()
        header = {'facilities': int(facilities), 'range': int(range)}
        
        # adiciona os pontos na lista
        for line in f:
            x, y = line.split()
            points.append({'x': int(x), 'y': int(y), 'visited': False})

    return header, points

# calcula a distancia euclidiana entre dois pontos
def distance(a, b):
    return sqrt(((a['x'] - b['x'])*(a['x'] - b['x'])) + ((a['y'] - b['y'])*(a['y'] - b['y'])))

# calcula o movimento de vizinhança
def movement(header, points, solutions):
    length = []
    # calcula o tamanho das soluções
    for solution in solutions:
        length.append(len(solution))
    
    # encontra a menor solução
    least_solution = min(length)
    min_point = solutions[length.index(least_solution)][0]

    for point in solutions[length.index(least_solution)]:
        point['visited'] = False

    # percorre todos os pontos não visitados procurando uma soluçao melhor
    for point in points:
        if point != min_point and not point['visited']:

            # adiciona o ponto na primeira posição da lista
            new_solution = [point]
            
            # marca como visitado
            point['visited'] = True

            # adiciona os outros pontos que estão no range
            for point2 in points:
                if not point2['visited'] and distance(point, point2) <= header['range']:
                    new_solution.append(point2)
                    point2['visited'] = True

            # verifica se a nova solução é melhor
            if (len(new_solution) > length[length.index(least_solution)]):
                solutions[length.index(least_solution)] = new_solution
                # retorna a lista com a solução encontrada
                return solutions
            else:
                for point in new_solution:
                    point['visited'] = False


    for point in solutions[length.index(least_solution)]:
        point['visited'] = True

# gera uma lista de soluções data um conjunto de pontos e número de facilities e range
def generate(header, points):
    solutions = []
    gul = []

    # monta um array com a quantidade de pontos cobertos para cada ponto na entrada
    for point in points:
        aux = []
        # adiciona o ponto na primeira posição da lista
        aux.append(point)
        # marca como visitado
        point['visited'] = True

        # adiciona os outros pontos que estão no range
        for point2 in points:
            if not point2['visited'] and distance(point2, point) <= header['range']:
                aux.append(point2)
        point['visited'] = False

        # coloca a tupla (ponto, quantidade de pontos cobertos) na lista
        gul.append([point, len(aux)])

    # ordena a lista pelos pontos que cobrem mais pontos
    gul = sorted(gul, key=lambda meh: meh[1], reverse=True)

    # monta a lista de soluções escolhida
    j = 0
    for i in range(header['facilities']):
        while gul[j][0]['visited'] == True:
            j += 1
            continue

        solutions.append([gul[j][0]])
        points[points.index(gul[j][0])]['visited'] = True
        
        for point in points:
            if not point['visited'] and distance(point, gul[j][0]) <= header['range']:
                solutions[i].append(point)
                point['visited'] = True
    
    return solutions, gul

def plot(solutions, points, header, title):
    # plt.plot([1,2,3,4], [1,4,9,16], 'ro')
    # plt.axis([0, 6, 0, 20])
    xs = []
    ys = []
    xs_facilities = []
    ys_facilities = []
    xs_visited = []
    ys_visited = []

    for solution in solutions:
        for point in solution:
            if point == solution[0]:
                xs_facilities.append(point['x'])
                ys_facilities.append(point['y'])
            else:
                xs_visited.append(point['x'])
                ys_visited.append(point['y'])
    
    for point in points:
        if point['visited'] is not True:
            xs.append(point['x'])
            ys.append(point['y'])

    plt.plot(xs_facilities, ys_facilities, 'yo', markersize=60, alpha=0.3)
    plt.plot(xs_visited, ys_visited, 'bo', markersize=2)
    plt.plot(xs, ys, 'bo', markersize=2)
    plt.title(title)
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.show()

def grasp(header, points, solutions, gulosa, loop, alpha):
    for i in range(loop):
        new_solution = []
        gul = gulosa[::]
        for point in points:
            point['visited'] = False
        for i in range(header['facilities']):
            parttempsolution = []
            rcl = makercl(alpha, gul)
            facility = randrange(0, len(rcl))
            parttempsolution.append(rcl[facility][0])
            gul.pop(gul.index(rcl[facility]))
            points[points.index(rcl[facility][0])]['visited'] = True
            for point in points:
                if not point['visited'] and distance(point, parttempsolution[0]) <= header['range']:
                    parttempsolution.append(point)
                    point['visited'] = True
                    for element in gul:
                        if element[0] == point:
                            gul.pop(gul.index(element))
            new_solution.append(parttempsolution)
        covered = 0
        for facility in solutions:
            covered += len(facility)
        solution = 0
        for facility in new_solution:
            solution += len(facility)
        if solution >= covered:
            solutions = new_solution
    return solutions

def makercl(alpha, gul):
    rcl = []
    for point in gul:
            if point[1] >= alpha*(gul[0][1] + gul[len(gul)-1][1]):
                rcl.append(point)
    return rcl

if __name__ ==  '__main__':
    # processa o arquivo passado
    header, points = readFile(sys.argv[1])
    # calcula a lista de soluções
    solutions, gul = generate(header, points)
    covered = 0
    for facility in solutions:
        #posição das facilities
        print('Posicao da facility (xy):', facility[0]['x'], facility[0]['y'], '|| Pontos cobertos:', len(facility))
        covered += len(facility)
    print ('Total de pontos cobertos:', covered)

    # executa o movimento de vizinhança
    new_solutions = movement(header, points, solutions)
    plot(new_solutions, points, header, 'solução gulosa (30 facilities)')
    aux_solutions = []
    while aux_solutions is not None:
        aux_solutions = movement(header, points, new_solutions)
        if aux_solutions is not None:
            new_solutions = aux_solutions
    covered = 0
    for facility in new_solutions:
        #posição das facilities
        print('Posicao da facility (xy):', facility[0]['x'], facility[0]['y'], '|| Pontos cobertos:', len(facility))
        covered += len(facility)
    print ('Total de pontos cobertos:', covered)
    plot(new_solutions, points, header, 'solução final (30 facilities)')
    grasp_solutions = grasp(header, points, solutions[::], gul[::], 5, 0.85)
    covered = 0
    for facility in grasp_solutions:
        #posição das facilities
        print('Posicao da facility (xy):', facility[0]['x'], facility[0]['y'], '|| Pontos cobertos:', len(facility))
        covered += len(facility)
    print ('Total de pontos cobertos:', covered)

