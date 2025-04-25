const video = document.createElement('video');
video.src = "http://localhost:8080/videos/video.mp4";
video.crossOrigin = "anonymous";
video.loop = true;
video.muted = true;
video.playsInline = true;

const audioVideo = document.getElementById('audio-video');
const canvas = document.getElementById('source');
const ctx = canvas.getContext('2d', { willReadFrequently: true });
const ascii = document.getElementById('ascii');

let w, h;

function getSliderValue(sliderId, randomId) {
    const slider = document.getElementById(sliderId);
    const randomCheckbox = document.getElementById(randomId);
    if (randomCheckbox && randomCheckbox.checked) {
        const min = parseFloat(slider.min);
        const max = parseFloat(slider.max);
        const step = parseFloat(slider.step) || 1;
        const randomValue = Math.round((min + Math.random() * (max - min)) / step) * step;
        slider.value = randomValue;
    }
    return parseFloat(slider.value);
}

function updateDimensions() {
    const fontSize = parseInt(document.getElementById('fontSizeSlider').value) || 9;
    const scaleY = getSliderValue('scaleYSlider', 'scaleYRandom') || 0.55;
    const charWidthEstimate = fontSize * 0.6;

    const isFullscreen = document.fullscreenElement === ascii;
    const containerWidth = isFullscreen ? window.innerWidth : ascii.parentElement.offsetWidth || window.innerWidth;

    w = Math.floor(containerWidth / charWidthEstimate);
    h = Math.floor(video.videoHeight * (w / video.videoWidth) * scaleY);

    canvas.width = w;
    canvas.height = h;
}

function renderFrameToAscii() {
    const glitchChance = getSliderValue('glitchSlider', 'glitchRandom') || 0.01;
    const contrast = getSliderValue('contrastSlider', 'contrastRandom') || 1;
    const brightness = getSliderValue('brightnessSlider', 'brightnessRandom') || 0;
    let chars = document.getElementById("charsetSelect").value;

    if (document.getElementById("invertCheckbox").checked) {
        chars = chars.split('').reverse().join('');
    }

    const fontSize = getSliderValue('fontSizeSlider', 'fontSizeRandom') || 9;
    ascii.style.fontSize = `${fontSize}px`;
    ascii.style.lineHeight = `${fontSize}px`;
    ascii.classList.toggle("shadow", document.getElementById("shadowCheckbox").checked);

    ctx.drawImage(video, 0, 0, w, h);
    const imageData = ctx.getImageData(0, 0, w, h);

    let asciiImage = '';
    for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
            const offset = (y * w + x) * 4;
            let r = imageData.data[offset];
            let g = imageData.data[offset + 1];
            let b = imageData.data[offset + 2];
            let avg = (r + g + b) / 3;
            avg = Math.min(255, Math.max(0, (avg + brightness) * contrast));
            const charIndex = Math.floor((avg / 255) * (chars.length - 1));
            asciiImage += chars[charIndex];
        }
        asciiImage += '\n';
    }

    ascii.innerHTML = asciiImage.split('').map(char => {
        const glitch = Math.random() < glitchChance;
        if (glitch && char.trim()) {
            return `<span style="animation: glitch 0.3s infinite;">${char}</span>`;
        }
        return char === '\n' ? '<br>' : char;
    }).join('');

    requestAnimationFrame(renderFrameToAscii);
}

// ▶️ Nuevo playVideos SIN delay
async function playVideos() {
    await Promise.all([
        video.play(),
        audioVideo.play()
    ]);
}

video.addEventListener('loadedmetadata', async () => {
    updateDimensions();
    requestAnimationFrame(renderFrameToAscii);

    try {
        await playVideos();
    } catch (error) {
        console.warn("Auto-play prevented. Waiting for first user interaction...");
        document.body.addEventListener('click', () => {
            playVideos();
        }, { once: true });
    }
});

function pauseVideos() {
    video.pause();
    audioVideo.pause();
}

function resetVideos() {
    video.currentTime = 0;
    audioVideo.currentTime = 0;
    playVideos();
}

document.getElementById('fullscreenBtn')?.addEventListener('click', () => {
    if (ascii.requestFullscreen) {
        ascii.requestFullscreen();
    } else if (ascii.webkitRequestFullscreen) {
        ascii.webkitRequestFullscreen();
    } else if (ascii.msRequestFullscreen) {
        ascii.msRequestFullscreen();
    }
});

document.addEventListener('fullscreenchange', () => {
    const isFullscreen = document.fullscreenElement === ascii;
    if (isFullscreen) {
        ascii.style.width = "100vw";
        ascii.style.height = "100vh";
        ascii.style.overflow = "hidden";
    } else {
        location.reload();
    }
    updateDimensions();
});
