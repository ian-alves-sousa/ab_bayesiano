from flask import Flask, render_template, redirect, url_for
import numpy as np
import pandas as pd

app = Flask(__name__)


@app.route('/home')
def index():
    return render_template('pg_layout_red.html')


@app.route('/yes', methods=['POST'])
def yes_event():
    df = pd.read_csv("../data/data_experiment.csv", delimiter=",")
    click = 1
    visit = 1
    group = 'treatment'

    df_raw = pd.DataFrame(
        {'click': click, 'visit': visit, 'group': group}, index=[0])
    df = pd.concat([df, df_raw])
    df.to_csv('../data/data_experiment.csv', index=False)
    return redirect(url_for('index'))


@app.route('/no', methods=['POST'])
def no_event():
    df = pd.read_csv("../data/data_experiment.csv", delimiter=",")
    click = 0
    visit = 1
    group = 'treatment'

    df_raw = pd.DataFrame(
        {'click': click, 'visit': visit, 'group': group}, index=[0])
    df = pd.concat([df, df_raw])
    df.to_csv('../data/data_experiment.csv', index=False)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5001)
