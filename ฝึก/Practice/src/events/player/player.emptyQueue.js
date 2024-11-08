module.exports = {
  name: "emptyQueue",
  execute(client, queue) {
    return client.say.queueEmbed(queue, "No more tracks to play, leaving now.");
  },
};
