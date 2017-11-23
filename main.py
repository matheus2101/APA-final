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
    
    return solutions



if __name__ ==  '__main__':
    # processa o arquivo passado
    header, points = readFile(sys.argv[1])
    # calcula a lista de soluções
    solutions = generate(header, points)
    covered = 0
    for facility in solutions:
        #posição das facilities
        print('Posicao da facility (xy):', facility[0]['x'], facility[0]['y'], '|| Pontos cobertos:', len(facility))
        covered += len(facility)
    print ('Total de pontos cobertos:', covered)
    # executa o movimento de vizinhança
    new_solutions = movement(header, points, solutions)
    for i in range(15):
        new_solutions = movement(header, points, new_solutions)
    covered = 0
    for facility in new_solutions:
        #posição das facilities
        print('Posicao da facility (xy):', facility[0]['x'], facility[0]['y'], '|| Pontos cobertos:', len(facility))
        covered += len(facility)
    print ('Total de pontos cobertos:', covered)
