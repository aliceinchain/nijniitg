document.addEventListener('DOMContentLoaded', (event) => {
    // Функция для вычисления среднего цвета изображения
    function getAverageColor(imgElement) {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        const width = imgElement.width;
        const height = imgElement.height;
        canvas.width = width;
        canvas.height = height;
        context.drawImage(imgElement, 0, 0, width, height);
        const imageData = context.getImageData(0, 0, width, height).data;
        let r = 0, g = 0, b = 0;
        for (let i = 0; i < imageData.length; i += 4) {
            r += imageData[i];
            g += imageData[i + 1];
            b += imageData[i + 2];
        }
        const pixelCount = imageData.length / 4;
        return { r: r / pixelCount, g: g / pixelCount, b: b / pixelCount };
    }

    // Функция для сортировки изображений по среднему цвету
    function sortImagesByColor() {
        const imageLinks = document.querySelectorAll('.image-link');
        const imagesArray = Array.from(imageLinks);
        imagesArray.sort((a, b) => {
            const colorA = getAverageColor(a.querySelector('img'));
            const colorB = getAverageColor(b.querySelector('img'));
            const brightnessA = (colorA.r + colorA.g + colorA.b) / 3;
            const brightnessB = (colorB.r + colorB.g + colorB.b) / 3;
            return brightnessA - brightnessB;
        });
        const container = document.getElementById('image-container');
        imagesArray.forEach(imgLink => container.appendChild(imgLink));
    }

    // Загрузка изображений и сортировка по цвету
    const imageLinks = document.querySelectorAll('.image-link img');
    let loadedImages = 0;
    imageLinks.forEach(img => {
        img.onload = () => {
            loadedImages++;
            if (loadedImages === imageLinks.length) {
                sortImagesByColor();
            }
        };
        img.onerror = () => {
            console.error(`Failed to load image: ${img.src}`);
            img.style.display = 'none'; // Скрыть изображение, если оно не загружается
        };
    });

    // Сортировка изображений при каждой перезагрузке страницы
    sortImagesByColor();

    // Функция для добавления проплывающих надписей
    function addFloatingText() {
        const container = document.getElementById('floating-text-container');
        fetch('phrases.txt')
            .then(response => response.text())
            .then(data => {
                const phrases = data.split('/');
                const maxPhrases = 5; // Максимальное количество одновременно отображаемых фраз
                let currentPhrases = [];

                function addPhrase() {
                    if (phrases.length === 0) return;
                    const phrase = phrases.shift();
                    const textElement = document.createElement('div');
                    textElement.className = 'floating-text';
                    textElement.textContent = phrase.trim();

                    // Случайное размещение текста по вертикали
                    const y = Math.random() * window.innerHeight;
                    textElement.style.top = `${y}px`;

                    container.appendChild(textElement);
                    currentPhrases.push(textElement);

                    // Удаление элемента после завершения анимации
                    textElement.addEventListener('animationend', () => {
                        container.removeChild(textElement);
                        currentPhrases = currentPhrases.filter(el => el !== textElement);
                        addPhrase(); // Добавление новой фразы
                    });
                }

                // Инициализация первых фраз
                for (let i = 0; i < maxPhrases; i++) {
                    addPhrase();
                }
            })
            .catch(error => console.error('Error loading phrases:', error));
    }

    // Добавление проплывающих надписей
    addFloatingText();
});
