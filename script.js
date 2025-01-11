document.addEventListener('DOMContentLoaded', (event) => {
    // Функция для загрузки изображений
    function loadImages() {
        const imageLinks = document.querySelectorAll('.image-link img');
        imageLinks.forEach(img => {
            img.onerror = () => {
                console.error(`Failed to load image: ${img.src}`);
                img.style.display = 'none'; // Скрыть изображение, если оно не загружается
            };
        });
    }

    // Загрузка изображений при загрузке страницы
    loadImages();
});
