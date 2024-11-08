const { ApplicationCommandOptionType } = require("discord.js");

module.exports = {
  name: "remove",
  description: "Remove a track from queue",
  category: "music",
  options: [
    {
      name: "index",
      description: "The track index to remove",
      type: ApplicationCommandOptionType.Number,
      required: true,
    },
  ],
  callback: (client, interaction, queue) => {
    if (queue.size < 1)
      return client.say.errorEmbed(interaction, "The queue has no more track.");

    const index = interaction.options.getNumber("index", true) - 1;

    if (index > queue.size || index < 0)
      return client.say.wrongEmbed(
        interaction,
        "Provided track index does not exist."
      );

    queue.node.remove(index);

    return client.say.successEmbed(interaction, `Removed track ${index + 1}.`);
  },
};
