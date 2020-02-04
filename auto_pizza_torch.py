import numpy as np
import random
import torch


def read_file(filepath):
    with open(filepath) as data_file:
        m, n = data_file.readline().split(' ')
        m, n = float(m), int(n)
        # m, n = torch.tensor(m), torch.tensor(n)
        sizes = [float(num) for num in data_file.readline().split(' ')]
        sizes = torch.tensor(sizes)
        return m, n, sizes


def get_score(m, n, all_s, selected):
    points = (all_s * (selected > 0.5)).sum()
    points = (points <= m) * points
    return points


def supersecretactivationfunctionhehe(x, scale):
    return (torch.tanh((x - 0.5) * scale) + 1) / 2


def get_nondiscrete_score(m, n, all_s, selected, scale):
    # points = np.sum(all_s[selected])
    selection = supersecretactivationfunctionhehe(selected, scale)
    hard_selection = selected > 0.5

    points = (all_s * selection).sum()
    hard_points = (all_s * hard_selection).sum()

    if hard_points > m:
        points = m - ((points - m))
        hard_points = 0

    return points, hard_points


def write_file(n, sample, filename):
    with open(filename, 'w') as result_file:
        result_file.write(str(n) + '\n')
        result_file.write(' '.join([str(s) for s in sample]) + '\n')


def get_loss_function(m):
    mse = torch.nn.MSELoss()
    zero = torch.tensor(0, dtype=torch.float)

    def loss(score):
        return (m - score) / m
    return loss


def compute_best(m, n, all_s):
    m, n = torch.tensor(m), torch.tensor(n)
    lr = 0.0001
    lr_decay = 1
    selected = torch.empty(n).normal_(mean=0.5, std=0.0001)
    selected.requires_grad_()
    # print(selected)
    loss_fun = get_loss_function(m)
    scale = 7
    for i in range(150):
        nondiscrete_score, score = get_nondiscrete_score(m, n, all_s, selected, scale=scale)
        print(i)
        print('Score: ', score, sep='\t')
        print('Nondiscrete: ', nondiscrete_score)
        if nondiscrete_score == m:
            break
        print('Selected: ', selected)
        loss = loss_fun(nondiscrete_score)
        print('Loss: ', loss)

        loss.requires_grad_()
        loss.backward()
        with torch.no_grad():
            selected -= selected.grad * lr
            print('Gradient:', selected.grad)
            selected.grad.zero_()
        lr *= lr_decay
        scale = scale + 0.8
        print(scale)
    print(selected)
    _, final_score = get_nondiscrete_score(m, n, all_s, selected, 500)
    return final_score


def main(filename):
    m, n, all_s = read_file(filename + '.in')
    scores = []
    for i in range(50):
        score = compute_best(m, n, all_s)
        scores.append(score)
    score_av = np.average(scores)
    print(score_av)


if __name__ == '__main__':
    main('a_example')
    # main('b_small')
    # main('c_medium')
    # main('d_quite_big')
    # main('e_also_big')
