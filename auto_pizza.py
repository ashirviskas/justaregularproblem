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
    points = np.sum(all_s[selected])
    if points <= m:
        return points
    else:
        return 0


def write_file(n, sample, filename):
    with open(filename, 'w') as result_file:
        result_file.write(str(n) + '\n')
        result_file.write(' '.join([str(s) for s in sample]) + '\n')


def main(filename):
    m, n, all_s = read_file(filename + '.in')
    best_score = 0
    best_sample = []
    for i in range(10000000):
        random_num_slices = random.randint(1965, 2000)
        random_sample = np.random.choice(n, random_num_slices, replace=False)
        score = get_score(m, n, all_s, random_sample)
        if score > best_score:
            best_sample = random_sample
            best_sample.sort()
            best_score = score
            print(score)
            print(random_num_slices)
    print('Best sample:', best_sample)
    print('Best score:', best_score)
    write_file(len(best_sample), best_sample, filename + '.out')


if __name__ == '__main__':
    # main('a_example')
    # main('b_small')
    # main('c_medium')
    main('d_quite_big')
    # main('e_also_big')
