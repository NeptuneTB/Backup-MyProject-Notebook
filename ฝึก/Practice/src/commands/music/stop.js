module.exports = {
  name: "stop",
  description: "Stop the playback.",
  category: "music",
  callback: async (client, interaction, queue) => {
    queue.delete();

    return client.say.successEmbed(interaction, "Stopped the playback.");
  },
};
