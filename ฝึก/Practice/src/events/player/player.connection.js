module.exports = {
  name: "connection",
  execute(client, queue) {
    const embed = client.utils
      .baseEmbed(queue)
      .setAuthor({ name: `${client.user.username}`, iconURL: client.user.displayAvatarURL() })
      .setDescription(
        `👍 Joined ${queue.channel.toString()} and 📄 bouned ${queue.metadata.toString()}`
      );

    return queue.metadata.send({ embeds: [embed] }).catch(console.error);
  },
};
