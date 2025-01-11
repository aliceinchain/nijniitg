document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    loadImages();
});

async function loadImages() {
    const response = await fetch('/images');
    const images = await response.json();
    const imageContainer = document.getElementById('imageContainer');
    imageContainer.innerHTML = '';

    images.forEach(image => {
        const img = document.createElement('img');
        img.src = image.url;

        const imageWrapper = document.createElement('a');
        imageWrapper.className = 'image-wrapper';
        imageWrapper.href = image.link;
        imageWrapper.target = '_blank';
        imageWrapper.appendChild(img);

        imageContainer.appendChild(imageWrapper);
    });
}

loadImages();
