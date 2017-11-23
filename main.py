import sys
from random import randrange
from math import sqrt

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

    # percorre todos os pontos procurando uma soluçao melhor
    for point in points:
        if point != min_point:

            # adiciona o ponto na primeira posição da lista
            new_solution = [point]
            
            # marca como visitado
            point['visited'] = True

            # adiciona os outros pontos que estão no range
            for point2 in points:
                if not point2['visited'] and  distance(point, point2) <= header['range']:
                    new_solution.append(point)
                    point['visited'] = True

            # verifica se a nova solução é melhor
            if (len(solution) > least_solution):
                solutions[least_solution] = new_solution
                # retorna a lista com a solução encontrada
                return solutions

# gera uma lista de soluções data um conjunto de pontos e número de facilities e range
def generate(header, points):
    solutions = []

    # executa uma vez para cada facility
    for i in range(header['facilities']):
        # escolhe uma posição inicial aleatória na lista de pontos
        position = randrange(0, len([points]))

        # verifica se o ponto na posição escolhida foi visitada
        # em caso afirmativo, escolhe outra posição
        while points[position]['visited']:
            position = randrange(0, len(points))
        
        # adiciona o ponto na primeira posição da lista
        solutions.append([points[position]])
        # marca como visitado
        points[position]['visited'] = True

        # adiciona os outros pontos que estão no range
        for point in points:
            if not point['visited'] and  distance(point, points[position]) <= header['range']:
                solutions[i].append(point)
                point['visited'] = True

    for facility in solutions:
        #posição das facilities
        print(facility[0]['x'], facility[0]['y'])
    
    return solutions



if __name__ ==  '__main__':
    # processa o arquivo passado
    header, points = readFile(sys.argv[1])
    # calcula a lista de soluções
    solutions = generate(header, points)
    # executa o movimento de vizinhança
    new_solutions = movement(header, points, solutions)