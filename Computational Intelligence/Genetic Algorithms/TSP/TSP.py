import random

class City():
    def __init__(self, index, X, Y):
        self.index = index
        self.X = X
        self.Y = Y

# CONFIG
##########################################################################################

CITIES = {}

CAPACITY = 0
GENE_SIZE = 0
HALF_GENE_SIZE = 0

with open("tsp_data.txt", "r") as f:
    for line in f:
        i, x, y = (float(x) for x in line.split(' '))
        CITIES.update({int(i): City(int(i), x, y)})
# Size of the genes to be mixed
GENE_SIZE = len(CITIES.items())
HALF_GENE_SIZE = GENE_SIZE // 2

# Size of initial population filled with some permutation of 0s and 1s
POP_SIZE = 50

# Maximum number of generations the algorithm will run
GEN_MAX = 2000

# END OF CONFIG
##########################################################################################

def pythagorian(first, second):
    one, two = CITIES.get(first), CITIES.get(second)
    return pow(pow(one.X - two.X, 2) + pow(one.Y - two.Y, 2), 0.5)

def fitness(target):
    distance = 0
    for i in range(len(target) - 1):
        distance += pythagorian(target[i], target[i + 1])
    return -distance

def spawn_starting_population(amount):
    population = []
    for _ in range(amount):
        chromosome = []
        cities_keys = list(CITIES.keys())
        for _ in range(GENE_SIZE):
            pick = random.choice(cities_keys)
            chromosome.append(pick)
            cities_keys.remove(pick)

        population.append(chromosome)

    return population
    
def two_randoms(target):
    return random.randint(0, len(target) - 1), random.randint(0, len(target) - 1)

# Swap Mutation
def mutate_swap(target):
    r1, r2 = 0, 0
    # To make sure our mutation actually mutates!
    while r1 == r2:
        r1, r2 = two_randoms(target)
    target[r1], target[r2] = target[r2], target[r1]

# Inverse Mutation
def mutate(target):
    r1, r2 = two_randoms(target)
    target[r1:r2] = target[r1:r2][::-1]

# Scramble Mutation
def mutate_scramble(target):
    r1, r2 = two_randoms(target)
    random.shuffle(target[r1:r2])

def tournament(fitnesses, k=10):
    amount = len(fitnesses) -1
    random_selections = [random.randint(0, amount) for _ in range(k)]
    random_fitnesses = {x: fitnesses[x] for x in random_selections}
    return max(random_fitnesses.keys(), key= lambda k: random_fitnesses[k])


def sort_by_fitness(population, is_reverse=True):
    return sorted(population, key=lambda x: fitness(x), reverse=is_reverse)

def fertilization(r1, r2, male, female):
    child = [0 for _ in range(GENE_SIZE)]
    child[r1:r2] = male[r1:r2]
    last = r2
    for i in range(last, last + GENE_SIZE):
        index = i % GENE_SIZE
        last = last % GENE_SIZE
        if female[index] not in child:
            child[last] = female[index]
            last += 1
    mutate(child)
    return child

def standard_deviation(fitnesses):
    N = len(fitnesses)
    mean = sum(fitnesses) / N
    nom = 0
    for value in fitnesses:
        nom += pow(value - mean, 2)
    return pow(nom / N, 0.5), mean

def crossover(population):
    # Preparation calculations
    fitnesses = []
    for person in population:
        fitnesses.append(fitness(person))
    # Sigma Scaling    
    c = 2
    sigma, mean = standard_deviation(fitnesses)
    for i in range(POP_SIZE):
        fitnesses[i] = fitnesses[i] - (mean - c * sigma)

    population_count = len(population)
    parent_count = population_count // 2

    # OX1 Crossover
    children = []
    for  _ in range(parent_count):
        male = population[tournament(fitnesses)]
        female = population[tournament(fitnesses)]
        r1, r2 = two_randoms(male)
        child1, child2 = fertilization(r1, r2, male, female), fertilization(r1, r2, female, male)
        children.append(child1)
        children.append(child2)

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

def graphize(solution):
    import matplotlib.pyplot as plt
    positions = []
    xpos, ypos = [], []
    for point in CITIES.values():
        positions.append([point.X, point.Y])
        xpos.append(point.X)
        ypos.append(point.Y)

    fig, ax = plt.subplots(2, sharex=True, sharey=True)         # Prepare 2 plots
    ax[0].set_title('Raw nodes')
    ax[1].set_title('Optimized tour')
    ax[0].scatter(xpos, ypos)             # plot A
    ax[1].scatter(xpos, ypos)             # plot B
    # distance = 0.
    start_node = solution[0]
    for i in range(len(solution) - 1):
        start_pos = positions[start_node - 1]
        next_node = solution[i + 1]
        end_pos = positions[next_node - 1]
        ax[1].annotate("",
                xy=start_pos, xycoords='data',
                xytext=end_pos, textcoords='data',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc3"))
        # distance += np.linalg.norm(end_pos - start_pos)
        start_node = next_node

    # textstr = "N nodes: %d\nTotal length: %.3f" % (N, distance)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax[1].text(0.05, 0.95, "", transform=ax[1].transAxes, fontsize=14, # Textbox
            verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.show()


def calculate():
    population = spawn_starting_population(POP_SIZE)
    for generation in range(1, GEN_MAX):
        print("Generation %d with %d chromosomes" % (generation, len(population)))
        population = sort_by_fitness(population, False)
        # for i in population:
        #     print("%s, fit: %s" % (str(i), fitness(i)))
        population = evolve_population(population)
    return population[0]

def main():
    solution = calculate()
    print ("Found answer after " + str(GEN_MAX) + " generations with fitness= " \
        + str (fitness(solution))
    )
    print(solution)
    graphize(solution)

if __name__ == "__main__":
    main()