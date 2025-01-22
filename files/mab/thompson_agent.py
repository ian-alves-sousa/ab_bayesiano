import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import beta


def reward_plot(success_array, failure_array):
    linestyle = ['-', '--']

    x = np.linspace(0, 1, 1002)[1:-1]

    plt.clf()
    plt.xlim(0, 1)
    plt.ylim(0, 30)

    for a, b, ls in zip(success_array, failure_array, linestyle):
        dist = beta(a, b)

        plt.plot(x, dist.pdf(x), ls=ls, c='black',
                 label=f'Alpha:{a}, Beta:{b}')
        plt.draw()
        plt.pause(0.00001)
        plt.legend(loc=0)


class ThompsonAgent(object):
    # prob_list sendo o valor da probabilidade de voltar 1, que seria definido ao instaciar a classe
    def __init__(self, prob_list):
        self.prob_list = prob_list

    def pull(self, bandit_machine):
        if np.random.random() < self.prob_list[bandit_machine]:
            reward = 1
        else:
            reward = 0
        return reward


# probabilidade de ter um resultado positivo da página
prob_list = [0.30, 0.35]

# parâmetros do experimento
trials = 1000
episodes = 200

# agent
bandit = ThompsonAgent(prob_list)

prob_reward_array = np.zeros(len(prob_list))
acculated_reward_array = list()
avg_acculated_reward_array = list()
for episode in range(episodes):

    success_array = np.ones(len(prob_list))
    failure_array = np.full(len(prob_list), 1.0e-5)

    reward_array = np.zeros(len(prob_list))
    bandit_array = np.full(len(prob_list), 1.0e-5)
    acculated_reward = 0
    for trial in range(trials):
        # agent - escolha
        # Com a distribuição beta é possível ver que quanto maior o número de tentativas, mais certeiro é o valor que a conversão converge
        prob_reward = np.random.beta(success_array, failure_array)
        bandit_machine = np.argmax(prob_reward)

        # agent - recompensa
        reward = bandit.pull(bandit_machine)

        if reward == 1:
            success_array[bandit_machine] += 1
        else:
            failure_array[bandit_machine] += 1

        # plot
        reward_plot(success_array, failure_array)

        # agent - guarda recompensa
        reward_array[bandit_machine] += reward
        bandit_array[bandit_machine] += 1
        acculated_reward += reward

    # calculando a probabilidade
    prob_reward_array += reward_array/bandit_array
    acculated_reward_array.append(acculated_reward)
    avg_acculated_reward_array.append(np.mean(acculated_reward_array))

prob01 = np.round(prob_reward_array[0]/episodes, 2)*100
prob02 = np.round(prob_reward_array[1]/episodes, 2)*100
# Retorna a probabilidade que a máquina voltou 1, sendo o valor definido na prob_list
print(f'\n Prob Bandit 01: {prob01}% - Prob Bandit 02: {prob02}%')
# Retorna a quantidade média de vezes que acertou no número de trials, no geral, é perto da média das duas probabilidades
print(f'\n Avg accumulated reward: {np.mean(avg_acculated_reward_array)}')
# Recompensa acumulada é sempre a metade do valor máximo que consegue
