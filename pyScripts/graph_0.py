import sys, getopt, json, copy

import plotly.plotly as py
from plotly.graph_objs import *

def graph(y_values):
    print y_values
    x_labels = ['0-5', '5-10', '10-30', '30-60', '60+']

    for since_v in 'since_win', 'since_loss':
        x_title = 'Minutes Since Last'
        x_title += ' Win' if since_v == 'since_win' else ' Loss'
        trace1 = Bar(
            x=x_labels,
            y=y_values['win'][since_v],
            name='Wins'
        )
        trace2 = Bar(
            x=x_labels,
            y=y_values['loss'][since_v],
            name='Losses'
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
        plot_url = py.plot(fig, filename=since_v)
        print plot_url

def main(argv):
    try:
        opts, args = getopt.getopt(argv, '')
    except getopt.GetoptError:
        print 'graph.py <file 1> <file 2> ...'
        sys.exit()
    calc_and_graph(args)

def init_y_vals():
    init_values = [0, 0, 0, 0, 0]
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
    elif val < 5*60:
        return 0
    elif val < 10*60:
        return 1
    elif val < 30*60:
        return 2
    elif val < 60*60:
        return 3
    else:
        return 4

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
