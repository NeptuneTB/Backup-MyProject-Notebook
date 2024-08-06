module.exports = {
  name: "disconnect",
  execute(client, queue) {
    return client.say.queueEmbed(queue, "Looks like my job here is done, leaving now.");
  },
};
