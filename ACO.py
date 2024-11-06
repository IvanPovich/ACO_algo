import random
import numpy as np

# Параметри алгоритму
NUM_ANTS, NUM_CITIES, ALPHA, BETA = 10, 5, 1.0, 5.0
EVAPORATION_RATE, Q, NUM_ITERATIONS = 0.5, 100, 100

# Матриця відстаней між містами
distance_matrix = np.array([
    [0, 2, 9, 10, 7],
    [1, 0, 6, 4, 3],
    [15, 7, 0, 8, 3],
    [6, 3, 12, 0, 11],
    [3, 9, 5, 7, 0]
])

pheromone_matrix = np.ones((NUM_CITIES, NUM_CITIES))

def choose_next_city(pheromone, distance, visited):
    tau_eta = [(pheromone[i] ** ALPHA) * ((1 / distance[i]) ** BETA) if i not in visited else 0 for i in range(NUM_CITIES)]
    probabilities = np.array(tau_eta) / sum(tau_eta)
    return np.random.choice(range(NUM_CITIES), p=probabilities)

def simulate_ant():
    visited, length = [random.randint(0, NUM_CITIES - 1)], 0
    while len(visited) < NUM_CITIES:
        current_city = visited[-1]
        next_city = choose_next_city(pheromone_matrix[current_city], distance_matrix[current_city], visited)
        length += distance_matrix[current_city][next_city]
        visited.append(next_city)
    length += distance_matrix[visited[-1]][visited[0]]
    return visited, length

def update_pheromones(paths):
    global pheromone_matrix
    pheromone_matrix *= (1 - EVAPORATION_RATE)
    for path, length in paths:
        for i in range(len(path) - 1):
            pheromone_matrix[path[i]][path[i + 1]] += Q / length
        pheromone_matrix[path[-1]][path[0]] += Q / length

best_path, best_length = None, float('inf')

for _ in range(NUM_ITERATIONS):
    paths = [simulate_ant() for _ in range(NUM_ANTS)]
    best_in_iter = min(paths, key=lambda x: x[1])
    if best_in_iter[1] < best_length:
        best_path, best_length = best_in_iter
    update_pheromones(paths)

print("Найкращий шлях:", list(map(int, best_path)), "\nДовжина:", best_length)
