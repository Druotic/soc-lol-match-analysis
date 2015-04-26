Pre-reqs: 

For pulling data from league API - must have mongodb running.


To run scrub.py - `sudo easy_install -f http://openmdao.org/dists bson` and scrub.py <file 1> ..<file n>.
<file 1>.scrubbed ... <file n>.scrubbed will be written.

For pulling data - `npm install` and `coffee pullData.coffee` and matches are written to mongo,
soc-lol-analysis database, players collection. Note: There is a bug I didn't take the time to fix - 
the program hangs when trying to pull multiple players data, it can only pull one player at a time.  So,
I pulled for one player, commented out that player, then ran for the next, and so on (for 10 players). If
extending this further to pull 100s or 1000s of players' match data, obviously this would need to be fixed.

players/<name>.json files are just sample data pulled from mongo after the API pull.
