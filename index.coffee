api = require 'leagueapi'
config = require './config'
# sync = require 'synchronize'
# {Player} = require './models/player'
redis = require 'redis'
# process = require 'process'

client = redis.createClient('6379', '127.0.0.1', {});
client.set("test", 10)
client.set("test", 5, (err) ->
  if err
    throw err
  console.log "SET!"
)
process.exit()

console.log config
api.init(config.apiKey, config.region)

client.on("error", (err) ->
  console.log "Redis Error: #{err}"
)

# update with smurf/alt IDs
summonerIDGroupsChallenger =
  dyrus: [5908]
  wildturtle: [521955, 18991200]
  pobelter: [2648]
  bjergsen: [63581619]
  imaqtpie: [19887289]
  wizfujin: [56403918]
  doublelift: [20132258]
  sneaky: [51405]
  meteos: [390600]
  shiphtur: [19967304]

# get later (need active players)
summonerIDGroupsSilver =
  foo: "bar"

storeHistory = (err, data) ->
  if err
    throw err
  return if Object.keys(data).length == 0
  date = new Date 0
  console.log data.matches.length
  client.get('currName', writeToDB)

writeToDB = (err, playerName) ->
  if err
    throw err
  Player.find({name: playerName}, (err, player) ->
    if err
      # if name not found, create new player
      player = new Player({name: playerName, matches: data.matches})
      player.save()
    else
      player.matches.push data.matches...
      player.save()
    client.incrby('lastIndex', data.matches.length)
    client.get('lastIndex', callAPI)
  )

callAPI = (err, idx) ->
  if err
    throw err
  options = {rankedQueues: ['RANKED_SOLO_5x5'], beginIndex: idx}
  console.log "calling api with options: #{options}"
  api.getMatchHistory(summonerID, options, config.region, storeHistory);

# to be used syncronously ONLY
mainSync = ->
  for name, ids in summonerIDGroupsChallenger
    client.set('currName', name)
    # call for each id, aggregate
    for id in ids
      client.set('lastIndex', 0)
      callAPI(null, 0)

sync(api, 'getMatchHistory')
sync(client, 'set', 'get')

sync.fiber(mainSync)
