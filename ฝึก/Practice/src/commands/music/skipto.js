const { ApplicationCommandOptionType } = require("discord.js");

module.exports = {
  name: "skipto",
  description: "Skip to the given track, removing others on the way",
  category: "music",
  options: [
    {
      name: "index",
      description: "The track index to skip to",
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

    queue.node.skipTo(index);

    return client.say.successEmbed(
      interaction,
      `Skipped to track ${index + 1}.`
    );
  },
};
