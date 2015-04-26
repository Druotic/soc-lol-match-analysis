import sys, getopt, bson

player_name = None

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
    matches = read_sort_matches(fn)
    print matches.name

def read_sort_matches(fn):
    matches = None
    with open(fn) as file:
        player = bson.loads(file)
        print str(player)
        player_name = player.name
        matches = player.matches
        matches = sorted(matches, key=lambda match: match.matchCreation , reverse=False)
    return {name: player_name, matches: matches}

if __name__ == "__main__":
    main(sys.argv[1:])
