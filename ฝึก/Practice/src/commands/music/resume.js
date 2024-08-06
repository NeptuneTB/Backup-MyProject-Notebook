module.exports = {
  name: "resume",
  description: "Resume the playback",
  category: "music",
  callback: (client, interaction, queue) => {
    if (queue.node.isPlaying())
      return client.say.wrongEmbed(interaction, "The playback is already playing.");

    queue.node.resume();

    return client.say.successEmbed(interaction, "Resumed the playback.");
  },
};
