import sys, getopt, json, copy

import plotly.plotly as py
from plotly.graph_objs import *

def graph(y_values):
    print y_values
    x_labels = ['0-5', '5-10', '10-15', '15-20', '20-25',
        '25-30', '30-35', '35-40', '40-45', '45-50', '50-55',
        '55-60', '60+']

    x_title = 'Minutes'
    trace1 = Bar(
        x=x_labels,
        y=[a-b for a,b in zip(y_values['win']['since_win'], y_values['loss']['since_win'])],
        name='Since Last Win'
    )
    trace2 = Bar(
        x=x_labels,
        y=[a-b for a,b in zip(y_values['win']['since_loss'], y_values['loss']['since_loss'])],
        name='Since Last Loss'
    )
    data = Data([trace1, trace2])
    layout = Layout(
        barmode='group',
        xaxis=XAxis(
            title=x_title
        ),
        yaxis=YAxis(
            title='Count'
        )
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='combined-diff')
    print plot_url

def main(argv):
    try:
        opts, args = getopt.getopt(argv, '')
    except getopt.GetoptError:
        print 'graph.py <file 1> <file 2> ...'
        sys.exit()
    calc_and_graph(args)

def init_y_vals():
    init_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # number of wins/losses in which the times since last win/loss fall into each time range
    y_values = {
        'win': {
            'since_win': list(init_values),
            'since_loss': list(init_values)
        },
        'loss': {
            'since_win': list(init_values),
            'since_loss': list(init_values)
        }
    }
    return y_values

# could improve, but leaving simple/messy for now.
def get_y_val_idx(val):
    if val < 0:
        return -1
    minutes_arr = [5,10,15,20,25,30,35,40,45,50,55,60]
    for idx, minutes in enumerate(minutes_arr):
        if val < minutes*60:
            return idx
    return len(minutes_arr)

# [<5 min, 5-10 min, 10-30min, 30-60min, 60+ min] for both win and loss returned
def calc_and_graph(files):
    total_matches = 0
    y_values = init_y_vals()
    for file in files:
        lines = None
        with open(file) as f:
            lines = f.readlines()
        for line in lines:
            if 'timeSinceWin' in line:
                continue
            total_matches += 1
            line_tok = line.split()
            key1 = 'win' if int(line_tok[1]) == 1 else 'loss'
            vals = y_values[key1]
            for since_v in 'since_win', 'since_loss':
                idx = 2 if since_v == 'since_win' else 3
                time_since = int(line_tok[idx])
                if time_since == -1:
                    continue
                y_val_idx = get_y_val_idx(int(time_since))
                vals[since_v][y_val_idx] += 1 if y_val_idx > -1 else 0
    print "total matches: " + str(total_matches)
    graph(y_values)

if __name__ == '__main__':
    main(sys.argv[1:])
#output format: <name> <win> <timeSinceWin> <timeSinceLoss>
