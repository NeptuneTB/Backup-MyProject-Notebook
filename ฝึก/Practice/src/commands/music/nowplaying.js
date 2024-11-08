module.exports = {
  name: "nowplaying",
  description: "Show the currently playing track.",
  category: "music",
  callback: (client, interaction, queue) => {
    const track = queue.currentTrack;

    const embed = client.utils
      .baseEmbed(interaction)
      .setAuthor({ name: "Nowplaying 🎵" })
      .setTitle(`${track.title}`)
      .setURL(`${track.url}`)
      .setThumbnail(`${track.thumbnail}`)
      .setDescription(`Played by: ${track.requestedBy.toString()}\n
${queue.node.createProgressBar()}`);

    return interaction.reply({ ephemeral: true, embeds: [embed] }).catch(console.error);
  },
};
