const { EmbedBuilder, Colors } = require("discord.js");

module.exports = {
  name: "error",
  execute(client, queue, error) {
    client.utils.sendErrorLog(client, error, "error");

    const embed = new EmbedBuilder()
      .setTitle("An error occured while playing")
      .setDescription(`Reason: \`${error.message}\``)
      .setColor(Colors.Red);

    return queue.metadata.send({ embeds: [embed] }).catch(console.error);
  },
};
