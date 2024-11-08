const { ApplicationCommandOptionType } = require("discord.js");

module.exports = {
  name: "trackinfo",
  description: "Show details of a track.",
  category: "music",
  options: [
    {
      name: "index",
      type: ApplicationCommandOptionType.Number,
      description: "That track index.",
      required: true,
    },
  ],
  callback: (client, interaction, queue) => {
    const index = interaction.options.getNumber("index", true) - 1;

    if (index > queue.size || index < 0)
      return client.say.errorEmbed(
        interaction,
        "Provided track Index does not exist."
      );

    const track = queue.tracks.toArray()[index];

    if (!track)
      return client.say.wrongEmbed(interaction, "The track was not found.");

    const embed = client.utils
      .baseEmbed(interaction)
      .setAuthor({ name: "Trackinfo 🎵" })
      .setTitle(`${track.title}`)
      .setURL(`${track.url}`)
      .setThumbnail(`${track.thumbnail}`)
      .setDescription(`~ Requested by: ${track.requestedBy.toString()}
Duration: ${track.duration}
Position in queue: ${index + 1}`);

    return interaction
      .reply({ ephemeral: true, embeds: [embed] })
      .catch(console.error);
  },
};
