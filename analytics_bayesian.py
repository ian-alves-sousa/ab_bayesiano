from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy import stats
import pandas as pd
import numpy as np


def bayesian_inference(df1):
    N_mc = 10000
    proba_b_better_a = []
    proba_a_better_b = []
    expected_loss_a = []
    expected_loss_b = []
    for day in range(len(df1)):

        u_a, var_a = stats.beta.stats(a=1 + df1.loc[day, 'acc_clicks_A'],
                                      b=1 +
                                      (df1.loc[day, 'acc_visits_A'] -
                                       df1.loc[day, 'acc_clicks_A']),
                                      moments='mv'
                                      )

        u_b, var_b = stats.beta.stats(a=1 + df1.loc[day, 'acc_clicks_B'],
                                      b=1 +
                                      (df1.loc[day, 'acc_visits_B'] -
                                       df1.loc[day, 'acc_clicks_B']),
                                      moments='mv'
                                      )

        # Amostras da distribuição Normal A
        x_a = np.random.normal(loc=u_a,
                               scale=1.25*np.sqrt(var_a),
                               size=N_mc)

        # Amostras da distribuição Normal A
        x_b = np.random.normal(loc=u_b,
                               scale=1.25*np.sqrt(var_b),
                               size=N_mc)

        # Beta distribution function of page A
        fa = stats.beta.pdf(x_a,
                            a=1 + df1.loc[day, 'acc_clicks_A'],
                            b=1 + (df1.loc[day, 'acc_visits_A'] -
                                   df1.loc[day, 'acc_clicks_A'])
                            )

        # Beta distribution function of page B
        fb = stats.beta.pdf(x_b,
                            a=1 + df1.loc[day, 'acc_clicks_B'],
                            b=1 + (df1.loc[day, 'acc_visits_B'] -
                                   df1.loc[day, 'acc_clicks_B'])
                            )

        # Normal distribution function of page A
        ga = stats.norm.pdf(x_a,
                            loc=u_a,
                            scale=1.25*np.sqrt(var_a)
                            )

        # Normal distribution function of page A
        gb = stats.norm.pdf(x_b,
                            loc=u_b,
                            scale=1.25*np.sqrt(var_b)
                            )

        # Bera/Normal
        y = (fa*fb)/(ga*gb)

        # Somente valores onde o B é maior que A
        yb = y[x_b >= x_a]
        ya = y[x_a >= x_b]

        # Probabilidade de B ser melhor do que A
        p_b = (1 / N_mc) * np.sum(yb)
        p_a = (1 / N_mc) * np.sum(ya)

        proba_b_better_a.append(p_b)
        proba_a_better_b.append(p_a)

        # Erro ao assumir B melhor do que A
        expected_loss_A = (1 / N_mc) * np.sum(((x_b - x_a)*y)[x_b >= x_a])
        expected_loss_B = (1 / N_mc) * np.sum(((x_a - x_b)*y)[x_a >= x_b])

        expected_loss_a.append(expected_loss_A)
        expected_loss_b.append(expected_loss_B)
    return proba_b_better_a, expected_loss_a, expected_loss_b


def animate(i):
    data = pd.read_csv('data_experiment.csv')

    # dtypes
    data['click'] = data['click'].astype('int')
    data['visit'] = data['visit'].astype('int')

    # pivot table
    data = data.reset_index().rename(columns={'index': 'day'})

    data = data.pivot(index='day', columns='group', values=[
                      'click', 'visit']).fillna(0).reset_index(drop=True)
    data.columns = ['click_control', 'click_treatment',
                    'visit_control', 'visit_treatment']
    data = data[['click_control', 'visit_control',
                 'click_treatment', 'visit_treatment']]

    data['acc_clicks_A'] = np.cumsum(data['click_control'])
    data['acc_visits_A'] = np.cumsum(data['visit_control'])
    data['acc_clicks_B'] = np.cumsum(data['click_treatment'])
    data['acc_visits_B'] = np.cumsum(data['visit_treatment'])

    # inference bayesian
    p, except_loss_a, except_loss_b = bayesian_inference(data)

    x1 = np.arange(len(p))

    plt.cla()
    plt.plot(x1, p, label='Probability B better A')
    plt.plot(x1, except_loss_a, label='Risk Choosing A')
    plt.plot(x1, except_loss_b, label='Risk Choosing B')
    plt.hlines(0.0001, 0, len(data), color='black', linestyle='--')
    plt.hlines(0.9, 0, len(data), color='red', linestyle='--')
    plt.legend(loc='upper right')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
