module.exports = {
  name: "playerSkip",
  execute(client, queue, track) {
    return client.say.queueEmbed(queue, `Skipping **${track.title}** due to an issue!`);
  },
};
