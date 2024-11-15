module.exports = {
  name: "audioTrackAdd",
  execute(client, queue, track) {
    const embed = client.utils
      .baseEmbed(queue)
      .setAuthor({ name: `Track queued - Position ${queue.node.getTrackPosition(track) + 1}` })
      .setTitle(`${track.title}`)
      .setURL(`${track.url}`)
      .setFooter({
        text: `Requested by: ${track.requestedBy.tag}`,
        iconURL: track.requestedBy.displayAvatarURL({ dynamic: true }),
      });

    return queue.metadata.send({ embeds: [embed] }).catch(console.error);
  },
};
