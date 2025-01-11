// Пример массива изображений и ссылок
const images = [
    { url: 'IMAGE_URL_1', link: 'LINK_1' },
    { url: 'IMAGE_URL_2', link: 'LINK_2' },
    // Добавьте больше изображений по мере необходимости
];

const imageContainer = document.getElementById('image-container');

images.forEach(image => {
    const a = document.createElement('a');
    a.href = image.link;
    a.className = 'image-link';
    a.target = '_blank';

    const img = document.createElement('img');
    img.src = image.url;
    img.alt = 'Image';

    a.appendChild(img);
    imageContainer.appendChild(a);
});
