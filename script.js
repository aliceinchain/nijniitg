document.getElementById('fileInput').addEventListener('change', handleFileSelect);

function handleFileSelect(event) {
    const files = event.target.files;
    const imageContainer = document.getElementById('imageContainer');

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;

                const imageWrapper = document.createElement('div');
                imageWrapper.className = 'image-wrapper';
                imageWrapper.appendChild(img);

                imageWrapper.addEventListener('click', function() {
                    alert('Image clicked!');
                });

                imageContainer.appendChild(imageWrapper);
            };
            reader.readAsDataURL(file);
        }
    }
}
