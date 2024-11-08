const { ApplicationCommandOptionType } = require("discord.js");

module.exports = {
  name: "jump",
  description:
    "Jump to specific track on the queue without removing other tracks",
  category: "music",
  options: [
    {
      name: "index",
      description: "The track index to jump to",
      type: ApplicationCommandOptionType.Number,
      required: true,
    },
  ],
  callback: (client, interaction, queue) => {
    if (queue.isEmpty())
      return client.say.errorEmbed(interaction, "The queue has no more track.");

    const index = interaction.options.getNumber("index", true) - 1;

    if (index > queue.size || index < 0)
      return client.say.wrongEmbed(
        interaction,
        "Provided track index does not exist."
      );

    queue.node.jump(index);

    return client.say.successEmbed(
      interaction,
      `Jumped to track ${index + 1}.`
    );
  },
};
