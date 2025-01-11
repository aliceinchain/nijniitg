const mongoose = require('mongoose');

const imageSchema = new mongoose.Schema({
    url: String,
    link: String
});

module.exports = mongoose.model('Image', imageSchema);
