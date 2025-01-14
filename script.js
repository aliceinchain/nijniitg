document.addEventListener('DOMContentLoaded', (event) => {
    // Добавляем функцию для анализа яркости изображения
    function getImageBrightness(imgElement) {
        return new Promise((resolve) => {
            const canvas = document.getElementById('analyzeCanvas');
            const ctx = canvas.getContext('2d');

            // Устанавливаем размер canvas
            canvas.width = imgElement.naturalWidth || imgElement.width;
            canvas.height = imgElement.naturalHeight || imgElement.height;

            // Рисуем изображение на canvas
            ctx.drawImage(imgElement, 0, 0);

            // Получаем данные пикселей
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;

            let brightness = 0;

            // Вычисляем среднюю яркость
            for(let i = 0; i < data.length; i += 4) {
                // Используем формулу: (R + G + B) / 3
                brightness += (data[i] + data[i + 1] + data[i + 2]) / 3;
            }

            // Возвращаем среднюю яркость
            resolve(brightness / (data.length / 4));
        });
    }

    // Функция сортировки изображений
    async function sortImagesByBrightness() {
        const container = document.getElementById('image-container');
        const links = Array.from(container.getElementsByClassName('image-link'));

        // Создаем массив промисов для анализа яркости
        const brightnessPromises = links.map(async (link) => {
            const img = link.querySelector('img');
            const brightness = await getImageBrightness(img);
            return { link, brightness };
        });

        // Ждем завершения всех промисов
        const results = await Promise.all(brightnessPromises);

        // Сортируем по яркости
        results.sort((a, b) => b.brightness - a.brightness);

        // Переупорядочиваем элементы
        results.forEach(result => {
            container.appendChild(result.link);
        });
    }

    // Добавляем обработчик для видео, чтобы оно повторялось
    const backgroundVideo = document.getElementById('background-video');
    backgroundVideo.loop = true;

    // Запускаем сортировку при загрузке всех изображений
    const images = document.querySelectorAll('#image-container img');
    let loadedImages = 0;

    images.forEach(img => {
        if (img.complete) {
            loadedImages++;
            if (loadedImages === images.length) {
                sortImagesByBrightness();
            }
        } else {
            img.addEventListener('load', () => {
                loadedImages++;
                if (loadedImages === images.length) {
                    sortImagesByBrightness();
                }
            });
        }
    });

    const audio = document.getElementById('background-audio');
    const volumeSlider = document.getElementById('volume-slider');
    const pauseButton = document.getElementById('pause-button');
    const startAudioButton = document.getElementById('start-audio-button');
    const infoPanel = document.getElementById('info-panel');
    const backgroundOverlay = document.getElementById('background-overlay');
    const blurOverlay = document.getElementById('blur-overlay');
    const textContainer = document.getElementById('floating-text-container');
    const trackSelect = document.getElementById('track-select');

    // Функция для создания плавающего текста
    function createFloatingText(text) {
        const floatingText = document.createElement('div');
        floatingText.className = 'floating-text';
        floatingText.textContent = text;

        // Случайная позиция по вертикали
        const yPosition = Math.random() * (window.innerHeight - 50);
        floatingText.style.top = `${yPosition}px`;

        // Случайная длительность анимации
        const duration = 15 + Math.random() * 10;
        floatingText.style.animation = `float ${duration}s linear`;

        textContainer.appendChild(floatingText);

        // Удаление элемента после завершения анимации
        floatingText.addEventListener('animationend', () => {
            floatingText.remove();
        });
    }

    // Загрузка фраз из файла
    fetch('phrases.txt')
        .then(response => response.text())
        .then(text => {
            const phrases = text.split('/').map(phrase => phrase.trim()).filter(phrase => phrase);

            // Создание новых фраз с интервалом
            setInterval(() => {
                const randomPhrase = phrases[Math.floor(Math.random() * phrases.length)];
                createFloatingText(randomPhrase);
            }, 3000);
        })
        .catch(error => console.error('Error loading phrases:', error));

    // Настройка аудиоплеера
    volumeSlider.value = audio.volume;
    volumeSlider.addEventListener('input', (event) => {
        audio.volume = event.target.value;
    });

    pauseButton.addEventListener('click', () => {
        if (audio.paused) {
            audio.play();
            pauseButton.textContent = 'АСТААНВИ МУЗЫКУУУ';
        } else {
            audio.pause();
            pauseButton.textContent = 'ВКЛЮЧИ ШАРМАНКУУ';
        }
    });

    startAudioButton.addEventListener('click', () => {
        infoPanel.style.display = 'none';
        backgroundOverlay.style.display = 'none';
        audio.play().catch(error => {
            console.error('Error playing audio:', error);
        });
    });

    trackSelect.addEventListener('change', () => {
        const selectedTrack = trackSelect.value;
        audio.src = selectedTrack;
        audio.play().catch(error => {
            console.error('Error playing audio:', error);
        });
    });

    infoPanel.style.display = 'flex';
    backgroundOverlay.style.display = 'block';

    // Эффект параллакса для видео
    document.addEventListener('mousemove', (e) => {
        const { clientX, clientY } = e;
        const x = clientX / window.innerWidth;
        const y = clientY / window.innerHeight;
        backgroundVideo.style.transform = `translate(-${x * 20}px, -${y * 20}px)`;
    });
});