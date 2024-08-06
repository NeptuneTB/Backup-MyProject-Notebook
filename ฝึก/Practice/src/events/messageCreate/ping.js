const { Client } = require('discord.js');
/**
 * 
 * @param {Client} client 
 */
module.exports = (client, message) => {
  if (message.content === 'ping') {
    const ping = Date.now() - message.createdTimestamp;

    message.channel.send(
      `Pong! Client ${ping}ms | Websocket: ${client.ws.ping}ms`
    );
  }
}