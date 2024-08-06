module.exports = {
  callback: (client, interaction, queue) => {
    if (queue.size < 1 && queue.repeatMode !== 3)
      return client.say.errorEmbed(interaction, "The queue has no more track.");

    queue.node.skip();

    return client.say.successEmbed(interaction, "Skipped the current track.");
  },

  name: "skip",
  description: "Skip current track",
  category: "music",
};
