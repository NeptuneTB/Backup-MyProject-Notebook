const { Schema, model } = require("mongoose");

const autoRoleSchema = new Schema({
  guildId: {
    type: String,
    require: true,
    unique: true,
  },
  roleId: {
    type: String,
    require: true,
  },
});

module.exports = model('AutoRole', autoRoleSchema)
