module.exports = {
  name: "audioTracksAdd",
  execute(client, queue, tracks) {
    const embed = client.utils
      .baseEmbed(queue)
      .setTitle(`${tracks.length} tracks queued.`)
      .setFooter({
        text: `Requested by: ${tracks[0].requestedBy.tag}`,
        iconURL: tracks[0].requestedBy.displayAvatarURL({ dynamic: true }),
      });

    return queue.metadata.send({ embeds: [embed] }).catch(console.error);
  },
};
