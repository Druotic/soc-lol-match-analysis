Introduction

League of Legends match history analysis completed as part of social computing course project. Some of this
code was written hastily, so there are some horribly copy/pasted areas (entire copies of graph.py for example).

There is also a bug with pullData.coffee (see below for more info) that I worked around via manual
intervention for the sake of time/delivery.


Pre-reqs: 

For pulling data from league API - must have mongodb running.

(For graphing) Create an account with Plotly - https://plot.ly/python/getting-started/ and setup credentials,
api key, etc.

Getting Started:

Install dependencies - `pip install -r pyScripts/requirements.txt`

To run scrub.py - `scrub.py <file 1> ..<file n>`
<file 1>.scrubbed ... <file n>.scrubbed will be written.

For pulling data - `npm install` and `coffee pullData.coffee` and matches are written to mongo,
soc-lol-analysis database, players collection. Note: There is a bug I didn't take the time to fix - 
the program hangs when trying to pull multiple players data, it can only pull one player at a time.  So,
I pulled for one player, commented out that player, then ran for the next, and so on (for 10 players). If
extending this further to pull 100s or 1000s of players' match data, obviously this would need to be fixed.

players/<name>.json files are just sample data pulled from mongo after the API pull
