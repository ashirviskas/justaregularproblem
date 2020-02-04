import numpy as np
import random
import torch


def read_file(filepath):
    with open(filepath) as data_file:
        m, n = data_file.readline().split(' ')
        m, n = float(m), int(n)
        m, n = torch.tensor(m), torch.tensor(n)
        sizes = [float(num) for num in data_file.readline().split(' ')]
        sizes = torch.tensor(sizes)
        return m, n, sizes


def get_score(m, n, all_s, selected):
    # points = np.sum(all_s[selected])
    points = (all_s * (selected > 0.5)).sum()
    points = (points <= m) * points
    # if points <= m:
    #     return points
    # else:
    #     return 0
    return points


def supersecretactivationfunctionhehe(x, scale):
    return (torch.tanh((x - 0.5) * scale) + 1) / 2


def get_nondiscrete_score(m, n, all_s, selected, scale):
    # points = np.sum(all_s[selected])
    selection = supersecretactivationfunctionhehe(selected, scale)
    hard_selection = supersecretactivationfunctionhehe(selected, 2 * scale)

    points = (all_s * selection).sum()
    hard_points = (all_s * hard_selection).sum()

    overpoint_penalty = 0


    # points = (points - m) * points
    # if points <= m:
    #     return points
    # else:
    #     return 0
    return points


def write_file(n, sample, filename):
    with open(filename, 'w') as result_file:
        result_file.write(str(n) + '\n')
        result_file.write(' '.join([str(s) for s in sample]) + '\n')


def get_loss_function(m):
    def loss(score):
        return (m - score) / m
    return loss


def compute_best(m, n, all_s):
    lr = 0.01
    lr_decay = 0.99
    selected = torch.empty(n).normal_(mean=0.5, std=0.001)
    selected.requires_grad_()
    # print(selected)
    loss_fun = get_loss_function(m)
    scale = 7
    for i in range(150):
        score = get_nondiscrete_score(m, n, all_s, selected, scale=10)
        print(i)
        print('Score: ', score)
        print('Selected: ', selected)
        loss = loss_fun(score)
        print('Loss: ', loss)

        loss.requires_grad_()
        loss.backward()
        with torch.no_grad():
            selected -= selected.grad * lr
            selected.grad.zero_()
        lr *= lr_decay
        scale *= 1.03
        print(scale)
    selected = torch.floor(selected + 0.5)
    print(selected)
    final_score = get_nondiscrete_score(m, n, all_s, selected, 500)
    return final_score


def main(filename):
    m, n, all_s = read_file(filename + '.in')
    scores = []
    for i in range(50):
        score = compute_best(m, n, all_s)
        scores.append(score.detach().numpy())
    score_av = np.average(scores)
    print(score_av)



if __name__ == '__main__':
    main('a_example')
    # main('b_small')
    # main('c_medium')
    # main('d_quite_big')
    # main('e_also_big')
