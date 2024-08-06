module.exports = {
  name: "replay",
  description: "Replay the current track.",
  category: "music",
  callback: (client, interaction, queue) => {
    queue.node.seek(0);

    return client.say.successEmbed(interaction, "Replayed the current track.");
  },
};
