const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const bodyParser = require('body-parser');
const Image = require('./models/Image');
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

mongoose.connect('mongodb://localhost:27017/clickable-images', { useNewUrlParser: true, useUnifiedTopology: true });

app.post('/upload', upload.single('image'), async (req, res) => {
    const { link } = req.body;
    const url = `/uploads/${req.file.filename}`;

    const image = new Image({ url, link });
    await image.save();

    res.json({ url, link });
});

app.get('/images', async (req, res) => {
    const images = await Image.find();
    res.json(images);
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
