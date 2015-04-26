import sys, getopt, json

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "")
    except getopt.GetoptError:
        print 'scrub.py <file 1> <file 2> ...'
        sys.exit()
    files = args
    print "Files being scrubbed: " + str(args)
    for file in files:
        scrub(file)

def scrub(fn):
    output_fn = fn + ".scrubbed"
    result = read_sort_matches(fn)
    player_name = result['name']
    matches = result['matches']
    last_win = -1
    last_loss = -1
    output_str = "name win timeSinceWin timeSinceLoss\n"
    for match in matches:
        output_str += player_name
        # convert to seconds (from ms)
        match_creation = match['matchCreation']/1000
        match_duration = match['matchDuration']
        end_time = match_creation + match_duration

        time_since_win = match_creation - last_win if last_win != -1 else -1
        time_since_loss = match_creation - last_loss if last_loss != -1 else -1
        # print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_win)) + " " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_loss))
        if match['participants'][0]['stats']['winner']:
            output_str += " 1"
            last_win = end_time
        else:
            output_str += " 0"
            last_loss = end_time
        output_str += " " + str(time_since_win) + " " + str(time_since_loss) + "\n"
    with open(output_fn, 'w') as f:
        print "writing to " + output_fn
        f.write(output_str)

def read_sort_matches(fn):
    player = None
    with open(fn) as file:
        player = json.load(file)
    matches = player['matches']
    matches = sorted(matches, key=lambda match: match['matchCreation'] , reverse=False)
    return {'name': player['name'], 'matches': matches}

if __name__ == "__main__":
    main(sys.argv[1:])


#output format: <name> <W/L> <timeSinceWin> <timeSinceLoss>
