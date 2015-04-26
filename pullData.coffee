api = require 'leagueapi'
config = require './config'
sync = require 'synchronize'
redis = require 'redis'

PlayerMeta = require './models/player'
Player = PlayerMeta.Player
playerMongoose = PlayerMeta.mongoose

# process = require 'process'

client = redis.createClient('6379', '127.0.0.1', {});

lastMatchIndex = 0
lastSummonerName = ""
lastSummonerID = 0


# client.set("test", 10)
# client.set("test", 5, (err) ->
#   if err
#     throw err
#   console.log "SET!"
# )
# process.exit()

console.log config
api.init(config.apiKey, config.region)

client.on("error", (err) ->
  console.log "Redis Error: #{err}"
)
client.on("end", () ->
  console.log "Closing Redis and Mongo Connections"
  playerMongoose.disconnect()
)

# update with smurf/alt IDs
summonerIDGroupsChallenger =
  # dyrus: [5908]
  # wildturtle: [521955, 18991200]
  # pobelter: [2648]
  # bjergsen: [51575588]
  # imaqtpie: [19887289]
  # wizfujin: [56403918]
  # doublelift: [20132258]
  # sneaky: [51405]
  # meteos: [390600]
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
  writeToDB(lastSummonerName, data.matches)

writeToDB = (playerName, matches) ->
  Player.findOne({name: playerName}, (err, player) ->
    if err
      throw err
      # if name not found, create new player
    else if not player
      player = new Player({name: playerName, matches: matches})
      player.save()
    else if player
      player.matches.push matches...
      player.save()
    lastMatchIndex += matches.length
    callAPI(lastMatchIndex)
  )

callAPI = (idx) ->
  options = {rankedQueues: ['RANKED_SOLO_5x5'], beginIndex: idx}
  console.log "calling api with options: #{JSON.stringify options}"
  console.log "name: " + lastSummonerName + " id: " + lastSummonerID
  api.getMatchHistory(lastSummonerID, options, config.region, storeHistory);
  console.log "after call"

# to be used syncronously ONLY
mainSync = ->
  for name, ids of summonerIDGroupsChallenger
    lastSummonerName = name
    # call for each id, aggregate
    for id in ids
      lastSummonerID = id
      lastMatchIndex = 0
      callAPI(lastMatchIndex)
  client.quit()

# Usually, this would be bad (sync), but performance is no concern in this case
sync(api, 'getMatchHistory')
sync(client, 'set', 'get')
callAPI = sync(callAPI)
writeToDB = sync(writeToDB)
storeHistory = sync(storeHistory)

sync.fiber(mainSync)
