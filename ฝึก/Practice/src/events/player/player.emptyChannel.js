module.exports = {
  name: "emptyChannel",
  execute(client, queue) {
    return client.say.queueEmbed(queue, "Feeling lonely, leaving now.");
  },
};
