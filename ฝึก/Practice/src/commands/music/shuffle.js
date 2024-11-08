module.exports = {
  name: "shuffle",
  description: "Shuffle the queue.",
  category: "music",
  callback: (client, interaction, queue) => {
    if (queue.size < 3)
      return client.say.wrongEmbed(
        interaction,
        "Need at least 3 tracks in the queue to shuffle."
      );

    queue.tracks.shuffle();

    return client.say.successEmbed(interaction, "Shuffled the queue.");
  },
};
