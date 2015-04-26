mongoose = require "mongoose"
mongoose.connect('mongodb://localhost/soc-lol-analysis')

playerSchema = new mongoose.Schema({
  name: String
  matches: []
})

exports.Player = mongoose.model('Player', playerSchema)
exports.mongoose = mongoose
