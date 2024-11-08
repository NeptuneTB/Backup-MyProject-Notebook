const { devs, testServer } = require("../../../config.json");
const getLocalCommands = require("../../utils/getLocalCommands");
const { Collection, PermissionsBitField } = require("discord.js");

module.exports = async (client, interaction, queue) => {
  if (!interaction.isChatInputCommand()) return;
  if (!interaction.inGuild()) return;
  const localCommands = getLocalCommands();

  // const cmdArg = interaction.commandName;
  // const command = client.commands.get(cmdArg);

  try {
    const commandObject = localCommands.find(
      (cmd) => cmd.name === interaction.commandName
    );

    if (!commandObject) return;
    if (!interaction.commandId) return;

    const userId = interaction.user.id;
    const { cooldowns } = client;

    if (!cooldowns.has(commandObject.name)) {
      cooldowns.set(commandObject.name, new Collection());
    }

    const now = Date.now();
    const timestamps = cooldowns.get(commandObject.name);
    const defaultCooldownDuration = 3;
    const cooldownAmount =
      (commandObject.cooldown ?? defaultCooldownDuration) * 1000;

    if (timestamps.has(userId)) {
      const expirationTime = timestamps.get(userId) + cooldownAmount;

      if (now < expirationTime) {
        const expiredTimestamp = Math.round(expirationTime / 1000);

        return interaction.reply({
          content: `You are on a cooldown for this command. You can use it again <t:${expiredTimestamp}:R>.`,
          ephemeral: true,
        });
      }
    }

    timestamps.set(userId, now);
    setTimeout(() => timestamps.delete(userId), cooldownAmount);

    if (
      !interaction.channel
        .permissionsFor(interaction.guild.members.me)
        .has(PermissionsBitField.Flags.EmbedLinks)
    )
      return interaction.reply({
        content: "I need **`Embed Links`** permission.",
        ephemeral: true,
      });

    if (
      (commandObject.category === "dev" || commandObject.devOnly === true) &&
      !botDevIds.includes(userId)
    ) {
      return interaction.reply({
        content: "This command can only be used by the bot developers.",
        ephemeral: true,
      });
    }

    if (commandObject.devOnly) {
      if (!devs.includes(interaction.member.id)) {
        interaction.reply({
          content: "Only developers are allowed to run this command.",
          ephemeral: true,
        });
        return;
      }
    }

    if (commandObject.testOnly) {
      if (interaction.guild.id !== testServer) {
        interaction.reply({
          content: "This command cannot be ran here.",
          ephemeral: true,
        });
        return;
      }
    }

    if (commandObject.permissionsRequired?.length) {
      for (const permission of commandObject.permissionsRequired) {
        if (!interaction.member.permissions.has(permission)) {
          interaction.reply({
            content: "Not enough permissions.",
            ephemeral: true,
          });
          return;
        }
      }
    }

    if (commandObject.botPermissions?.length) {
      for (const permission of commandObject.botPermissions) {
        const bot = interaction.guild.members.me;

        if (!bot.permissions.has(permission)) {
          interaction.reply({
            content: "I don't have enough permissions.",
            ephemeral: true,
          });
          return;
        }
      }
    }

    if (commandObject.category === "music" && commandObject.name !== "play") {
      const { useQueue } = require("discord-player");
      const queue = useQueue(interaction.guild.id);

      if (!queue)
        return interaction.reply({
          content: "I’m currently not playing in this server.",
          ephemeral: true,
        });

      const memberChannelId = interaction.member?.voice?.channelId;
      const queueChannelId = queue?.channel.id;

      if (!memberChannelId)
        return interaction.reply({
          content: "You need to join a voice channel first!",
          ephemeral: true,
        });

      if (memberChannelId !== queueChannelId)
        return interaction.reply({
          content: "You must be in the same voice channel as me!",
          ephemeral: true,
        });

      await commandObject.callback(client, interaction, queue);
    }

    await commandObject.callback(client, interaction);
  } catch (error) {
    console.log(`There was an error running this command: ${error}`);
  }
};
