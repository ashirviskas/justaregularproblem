import numpy as np
import random


def read_file(filepath):
    with open(filepath) as data_file:
        m, n = data_file.readline().split(' ')
        m, n = int(m), int(n)
        sizes = [int(num) for num in data_file.readline().split(' ')]
        sizes = np.array(sizes)
        return m, n, sizes


def get_score(m, n, all_s, selected):
    points = (all_s * selected).sum()
    if points <= m:
        return points
    else:
        return 0


def mutate(selected, mutation_percent):
    to_mutate = int(len(selected) * mutation_percent / 100)
    to_mutate = np.random.choice(len(selected), to_mutate//2, replace=False)
    selected[to_mutate] = (selected[to_mutate] - 1) * (-1)
    return selected


def breed(a, b, percent=25):
    to_mutate = np.random.choice(len(a), int(len(a) * percent / 100), replace=False)
    new_arr = np.copy(b)
    new_arr[to_mutate] = a[to_mutate]
    return new_arr


def write_file(n, sample, filename):
    with open(filename, 'w') as result_file:
        result_file.write(str(n) + '\n')
        result_file.write(' '.join([str(s) for s in sample]) + '\n')


def sort_scores(scores):
    return scores[np.argsort(scores[:, 1])[::-1]]


def breed_and_mutate(population, scores, breed_pop=50, mutate_pop=20, recreate=10):
    mutate_range = (len(scores) - mutate_pop, len(scores))
    breed_range = (len(scores) - mutate_pop - breed_pop, len(scores) - mutate_pop)
    to_breed_with = (0, len(scores) - (breed_pop + mutate_pop))
    # mutating
    for i in range(*mutate_range):
        to_mutate_id = scores[i, 0]
        population[to_mutate_id] = mutate(population[to_mutate_id], mutation_percent=4)
    # breeding
    for i in range(*breed_range):
        bad_an_id = scores[i, 0]
        good_an_id = scores[np.random.randint(*to_breed_with), 0]
        population[bad_an_id, :] = breed(population[good_an_id], population[bad_an_id], percent=15)


    # # recreating
    # for i in range()


def main(filename):
    m, n, all_s = read_file(filename + '.in')
    population_size = 100
    population = []
    for j in range(population_size):
        random_num_slices = random.randint(0, n)
        random_sample = np.random.choice(n, random_num_slices, replace=False)
        animal = np.zeros(n, dtype=np.int)
        animal[random_sample] = 1
        population.append(animal)
    population = np.array(population)

    for i in range(1000):
        scores = np.zeros((population_size, 2), dtype=np.int)
        for j, animal in enumerate(population):
            score = get_score(m, n, all_s, animal)
            scores[j, 0] = j
            scores[j, 1] = score
        scores = sort_scores(scores)
        print(scores[0])
        breed_and_mutate(population, scores, breed_pop=70, mutate_pop=20)
    best_s = scores[0, 0]
    print('Best sample:', scores[0, 0])
    print('Best score:', scores[0, 1])
    write_file(population[best_s].sum(), best_sample, filename + '.out')


if __name__ == '__main__':
    # main('a_example')
    # main('b_small')
    # main('c_medium')
    main('d_quite_big')
    # main('e_also_big')
