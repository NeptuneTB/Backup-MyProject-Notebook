const { ApplicationCommandOptionType } = require("discord.js");

module.exports = {
  name: "move",
  description: "Move a track in the queue",
  category: "music",
  options: [
    {
      name: "from",
      description: "The track to move",
      type: ApplicationCommandOptionType.Number,
      required: true,
    },
    {
      name: "to",
      description: "The position to move to",
      type: ApplicationCommandOptionType.Number,
      required: true,
    },
  ],
  callback: (client, interaction, queue) => {
    if (queue.size < 3)
      return client.say.errorEmbed(
        interaction,
        "Need at least 3 songs in the queue to use this command."
      );

    const from = interaction.options.getNumber("from", true);
    const to = interaction.options.getNumber("to", true);

    if (from < 1 || from >= queue.size)
      return client.say.wrongEmbed(
        interaction,
        "Provided `from` index is not valid."
      );

    if (to < 1 || to >= queue.size)
      return client.say.wrongEmbed(
        interaction,
        "Provided `to` position is not valid."
      );

    if (from === to)
      return client.say.wrongEmbed(
        interaction,
        "The track is already in this position."
      );

    queue.node.move(from, to);

    return client.say.successEmbed(
      interaction,
      `The track is moved to the position ${to}.`
    );
  },
};
