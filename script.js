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
                const phrases = data.split('/').map(phrase => phrase.trim()).filter(phrase => phrase);
                const maxPhrases = 4; // Максимальное количество одновременно отображаемых фраз
                let currentPhrases = [];

                function addPhrase() {
                    if (phrases.length === 0) return;
                    const randomIndex = Math.floor(Math.random() * phrases.length);
                    const phrase = phrases[randomIndex];

                    const textElement = document.createElement('div');
                    textElement.className = 'floating-text';
                    textElement.textContent = phrase;

                    // Случайное размещение текста по вертикали
                    const y = Math.random() * window.innerHeight;
                    textElement.style.top = `${y}px`;

                    // Случайное время исчезновения (до 5 секунд)
                    const animationDuration = Math.random() * 5 + 5; // от 5 до 10 секунд
                    textElement.style.animationDuration = `${animationDuration}s`;

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

    // Воспроизведение аудио
    const audio = document.getElementById('background-audio');
    const volumeSlider = document.getElementById('volume-slider');
    const pauseButton = document.getElementById('pause-button');
    const startAudioButton = document.getElementById('start-audio-button');
    const infoPanel = document.getElementById('info-panel');
    const backgroundOverlay = document.getElementById('background-overlay');
    const blurOverlay = document.getElementById('blur-overlay');

    // Управление громкостью
    volumeSlider.value = audio.volume;
    volumeSlider.addEventListener('input', (event) => {
        audio.volume = event.target.value;
    });

    // Управление паузой/воспроизведением
    pauseButton.addEventListener('click', () => {
        if (audio.paused) {
            audio.play();
            pauseButton.textContent = 'Pause';
        } else {
            audio.pause();
            pauseButton.textContent = 'Play';
        }
    });

    // Показать панель и воспроизвести аудио при нажатии на кнопку
    startAudioButton.addEventListener('click', () => {
        infoPanel.style.display = 'none';
        backgroundOverlay.style.display = 'none';
        blurOverlay.style.display = 'none';
        audio.play().catch(error => {
            console.error('Error playing audio:', error);
        });
    });

    // Показать панель при загрузке страницы
    infoPanel.style.display = 'flex';
    backgroundOverlay.style.display = 'block';
    blurOverlay.style.display = 'block';
});
