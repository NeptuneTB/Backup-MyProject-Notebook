module.exports = {
  callback: (client, interaction, queue) => {
    if (queue.node.isPaused())
      return client.say.wrongEmbed(
        interaction,
        "The playback is already paused."
      );

    queue.node.pause();

    return client.say.successEmbed(interaction, "Paused the playback.");
  },

  name: "pause",
  description: "Pause the playback",
  category: "music",
};
