const { ActivityType } = require('discord.js');

module.exports = (client) => {
  client.user.setActivity({
    name: 'NeptuneTestBot',
    type: ActivityType.Playing,
  });
}