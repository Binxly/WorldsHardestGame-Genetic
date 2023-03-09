import random
import copy

from game import GameInput, GameData

POPULATION_SIZE = 20
GENERATIONS = 100
MUTATION_RATE = 0.05

def create_player():
    # return a randomly generated player
    return [random.choice(["up", "down", "left", "right"]) for _ in range(100)]

def evaluate_player(player):
    # play the game with the given player and return the fitness score
    game_data = GameData()
    game_input = GameInput()

    for action in player:
        getattr(game_input, action)()
        game_data.update()

        if game_data.is_game_over():
            break

    return game_data.get_fitness()

def crossover(parent1, parent2):
    # create a new player by crossing over two parents
    child = copy.deepcopy(parent1)
    crossover_point = random.randint(0, len(parent1) - 1)
    child[crossover_point:] = parent2[crossover_point:]
    return child

def mutate(player):
    # randomly mutate a few actions in the player's sequence
    for i in range(len(player)):
        if random.random() < MUTATION_RATE:
            player[i] = random.choice(["up", "down", "left", "right"])
    return player

def create_next_generation(population):
    # select the best players from the current generation
    best_players = sorted(population, key=evaluate_player, reverse=True)[:POPULATION_SIZE // 2]

    # create the next generation by crossover and mutation
    next_generation = []
    for i in range(POPULATION_SIZE // 2):
        parent1 = random.choice(best_players)
        parent2 = random.choice(best_players)
        child = crossover(parent1, parent2)
        child = mutate(child)
        next_generation.append(child)

    # add some copies of the best players to the next generation
    for player in best_players:
        next_generation.extend([copy.deepcopy(player) for _ in range(POPULATION_SIZE // len(best_players) - 1)])

    return next_generation

def main():
    # create the initial population
    population = [create_player() for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        # create the next generation
        population = create_next_generation(population)

        # print the best player in the current generation
        best_player = max(population, key=evaluate_player)
        best_score = evaluate_player(best_player)
        print(f"Generation {generation}: Best score={best_score:.2f}")

if __name__ == "__main__":
    main()
