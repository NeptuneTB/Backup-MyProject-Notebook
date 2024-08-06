const glob = require("glob");

module.exports = function loadEvents(client) {
  const eventFiles = glob.sync("./src/events/player/*.js");

  for (const file of eventFiles) {
    const event = require(`../../${file}`);

    let type = "bot";
    if (file.includes("player.")) type = "player";

    if (type === "player") {
      const { useMainPlayer } = require("discord-player");
      const player = useMainPlayer();

      player.events.on(event.name, event.execute.bind(null, client));
    } else if (event.once) {
      client.once(event.name, event.execute.bind(null, client));
    } else {
      client.on(event.name, event.execute.bind(null, client));
    }

    delete require.cache[require.resolve(`../../${file}`)];

    // debug
    // client.logger.debug("EVENTS", `Loaded ${type}: ${event.name}`);
  }
};
