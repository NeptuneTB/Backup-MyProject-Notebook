module.exports = {
  name: "clear",
  description: "Clear the tracks in the queue.",
  category: "music",
  callback: (client, interaction, queue) => {
    if (queue.size < 2)
      return client.say.errorEmbed(interaction, "The queue has no more track.");

    queue.tracks.clear();

    return client.say.successEmbed(interaction, "Cleared the queue tracks.");
  },
};
