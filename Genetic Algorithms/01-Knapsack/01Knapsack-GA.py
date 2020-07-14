import random

class Item():
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

# CONFIG
##########################################################################################

ITEMS = []
CAPACITY = 0
GENE_SIZE = 0
HALF_GENE_SIZE = 0

def initialize(file_str):
    global CAPACITY, ITEMS, GENE_SIZE, HALF_GENE_SIZE
    ITEMS = []
    with open(file_str, "r") as f:
        _, CAPACITY = (int(x) for x in f.readline().split(' '))
        for line in f:
            x, y = (int(x) for x in line.split(' '))
            ITEMS.append(Item(x, y))
    # Size of the genes to be mixed
    GENE_SIZE = len(ITEMS)
    HALF_GENE_SIZE = GENE_SIZE // 2

# Size of initial population filled with some permutation of 0s and 1s
POP_SIZE = 100

# Maximum number of generations the algorithm will run
GEN_MAX = 500

# Start initial population with only zeros? If not, random permutation of 0s and 1s will be given
# Starting with 0s and 1s will generally make you find a good solution faster
START_POP_WITH_ZEROES = True

# END OF CONFIG
##########################################################################################


def fitness(target):
    """
    fitness(target) will return the fitness value of permutation named "target".
    Higher scores are better and are equal to the total value of items in the permutation.
    If total_weight is higher than the capacity, return 0 because the permutation cannot be used.
    """
    total_value = 0
    total_weight = 0
    for index, i in enumerate(target):
        if index >= len(ITEMS):
            break
        if i == 1:
            total_value += ITEMS[index].value
            total_weight += ITEMS[index].weight
        index += 1

    if total_weight > CAPACITY:
        return 0
    else:
        return total_value


def spawn_starting_population(amount):
    return [spawn_individual() for x in range(amount)]


def spawn_individual():
    if START_POP_WITH_ZEROES:
        return [random.randint(0, 0) for x in range(GENE_SIZE)]
    else:
        return [random.randint(0, 1) for x in range(GENE_SIZE)]


def mutate(target):
    """
    Changes a random element of the permutation array from 0 -> 1 or from 1 -> 0.
    """
    r = random.randint(0, len(target) - 1)
    if target[r] == 1:
        target[r] = 0
    else:
        target[r] = 1

# Finding parents using roulette wheel
def weighted_random_choice(choices, max):
    pick = random.uniform(0, max)
    current = 0
    for index, value in enumerate(choices):
        current += value
        if current > pick:
            return index
    return choices[random.randint(0, len(choices) - 1)]


def sort_by_fitness(population, is_reverse=True):
    return sorted(population, key=lambda x: fitness(x), reverse=is_reverse)


def crossover(population):
    fitnesses = []
    for person in population:
        fitnesses.append(fitness(person))
    sum_fitnesses = sum(fitnesses)

    population_count = len(population)
    # To make sure there are an even number of parents. 
    parent_count = (population_count // 2) - (population_count % 2)

    # one-point crossover
    children = []
    for _ in range(parent_count):
        male = population[weighted_random_choice(fitnesses, sum_fitnesses)]
        female = population[weighted_random_choice(fitnesses, sum_fitnesses)]
        child = male[:HALF_GENE_SIZE] + female[HALF_GENE_SIZE:]
        mutate(child)
        children.append(child)
    return sort_by_fitness(children)


def survival_selection(population, children):
    # Fitness-based survival selection
    new_population = []
    # The child to replace old and useless people
    child_index = 0
    out_of_children = False
    for elderly in population:
        current_child = children[child_index]
        if fitness(current_child) >= fitness(elderly) and not out_of_children:
            new_population.append(current_child)
            child_index += 1
            if child_index == len(children):
                out_of_children = True
                child_index -= 1
        else:
            new_population.append(elderly)
    return new_population


def evolve_population(population):
    
    children = crossover(population)
    new_population = survival_selection(population, children)

    return sort_by_fitness(new_population)



def calculate():
    population = spawn_starting_population(POP_SIZE)
    for _ in range(1, GEN_MAX):
        # print("Generation %d with %d" % (generation, len(population)))
        population = sort_by_fitness(population, False)
        # for i in population:
        #     print("%s, fit: %s" % (str(i), fitness(i)))
        population = evolve_population(population)
    return population[0]

def main():
    for i in range(1, 4):
        initialize("knapsack_%d.txt" % i)
        found_answer = calculate()
        print ("Found answer after " + str(GEN_MAX) + " generations for file #" + str(i) + " with fitness= " \
            + str (fitness(found_answer))
        )
        print(found_answer)

if __name__ == "__main__":
    main()