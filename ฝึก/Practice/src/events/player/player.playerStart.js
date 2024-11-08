module.exports = {
  name: "playerStart",
  execute(client, queue, track) {
    if (!track.requestedBy) track.requestedBy = client.user;

    const embed = client.utils
      .baseEmbed(queue)
      .setAuthor({ name: "Now playing" })
      .setTitle(`${track.title}`)
      .setURL(`${track.url}`)
      .setThumbnail(`${track.thumbnail}`)
      .setFooter({
        text: `Played by: ${track.requestedBy.tag}`,
        iconURL: `${track.requestedBy.displayAvatarURL({ dynamic: true })}`,
      });

    return queue.metadata.send({ embeds: [embed] });
  },
};
