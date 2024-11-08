require("dotenv").config();
const mongoose = require("mongoose");
const {
  Client,
  Collection,
  IntentsBitField,
  GatewayIntentBits,
} = require("discord.js");
const eventHandler = require("./handlers/eventHandler");
const { Player } = require("discord-player");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildVoiceStates,
    IntentsBitField.Flags.GuildMembers,
    IntentsBitField.Flags.GuildMessages,
    IntentsBitField.Flags.GuildPresences,
    IntentsBitField.Flags.MessageContent,
  ],
});

client.commands = new Collection();
client.cooldowns = new Collection();

client.utils = require("./modules/utils");
client.say = require("./modules/reply");

const player = Player.singleton(client);
player.extractors.loadDefault();

require("./handlers/Event")(client);

async function run() {
  try {
    await mongoose.connect(process.env.MONGODB_URI);
    console.log("Connected to DB.");

    eventHandler(client);
  } catch (error) {
    console.log(error);
  }
}
run().catch(console.dir);

client.login(process.env.TOKEN);
