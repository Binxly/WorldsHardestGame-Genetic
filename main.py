import os
import sys
import time
import json
import random

from selenium import webdriver

# local config.py
import config
from game import *

POPULATION_SIZE = 10
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.5
GENERATIONS = 100


class Individual:
    def __init__(self, genotype=None):
        if genotype is None:
            self.genotype = [random.choice(["up", "left", "down", "right"]) for _ in range(8)]
        else:
            self.genotype = genotype
        self.fitness = None

    def evaluate_fitness(self):
        game = GameData(self.genotype)
        self.fitness = get_fitness(game)

    def mutate(self):
        for i in range(len(self.genotype)):
            if random.random() < MUTATION_RATE:
                self.genotype[i] = random.choice(["up", "left", "down", "right"])

    def crossover(self, other):
        if random.random() < CROSSOVER_RATE:
            crossover_point = random.randint(0, len(self.genotype) - 1)
            new_genotype = self.genotype[:crossover_point] + other.genotype[crossover_point:]
            return Individual(new_genotype)
        else:
            return None

def get_fitness(game):
    return (1 / game.end_distance) + (game.collected_coins / 135) + (game.level * 2)


def main():
    # Create driver with all the arguments
    options = webdriver.ChromeOptions()
    # to leave browser open
    options.add_experimental_option("detach", True)
    options.add_argument("--log-level=%d" % int(config.driver_log_level))
    options.add_argument("--window-size=900,800")
    if config.driver_headless:
        options.add_argument("headless")

    driver = webdriver.Chrome(
        config.driver_path, service_log_path="driver.log", options=options
    )

    real_url = "file://" + os.path.join(os.getcwd(), config.base_url)
    driver.implicitly_wait(10)

    print(real_url)
    # Go to the url
    driver.get(real_url)

    data = GameData(driver)
    do = GameInput(driver)

    print(type(data.get_data()))
    print(data.get_data())
    print(get_fitness(data))

    do.up()
    do.left()
    do.down()
    do.right()
    do.up()
    do.left()
    do.down()
    do.right()

    driver.implicitly_wait(10)

    time.sleep(1)

    driver.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by the user.")
        sys.exit()
