import numpy as np


class RandomAgent(object):
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
prob_list = [0.3, 0.8]

# parâmetros do experimento
trials = 1000
episodes = 200

# agent
bandit = RandomAgent(prob_list)

prob_reward_array = np.zeros(len(prob_list))
acculated_reward_array = list()
avg_acculated_reward_array = list()
for episode in range(episodes):

    reward_array = np.zeros(len(prob_list))
    bandit_array = np.full(len(prob_list), 1.0e-5)
    acculated_reward = 0
    for trial in range(trials):
        # agent - escolha
        bandit_machine = np.random.randint(low=0, high=2, size=1)[0]

        # agent - recompensa
        reward = bandit.pull(bandit_machine)

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
#Recompensa acumulada é sempre a metade do valor máximo que consegue