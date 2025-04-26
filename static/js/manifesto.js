// manifesto.js

const canvas = document.getElementById('backgroundCanvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });

let width, height;
let particle;
const noiseDensity = 0.02;

function resizeCanvas() {
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

function createParticle() {
  const angle = Math.random() * 2 * Math.PI;
  const speed = Math.random() * 5 + 3;
  return {
    x: Math.random() * width,
    y: Math.random() * height,
    vx: Math.cos(angle) * speed,
    vy: Math.sin(angle) * speed,
    length: Math.random() * 10 + 5,
    baseOpacity: Math.random() * 0.3 + 0.3,
    opacity: 0,
    type: 'spiral',
    curve: Math.random() * 0.5 - 0.25,
    zigzagCounter: 0,
    angleOffset: Math.random() * Math.PI * 2,
    spiralDirection: Math.random() < 0.5 ? 1 : -1,
    life: 600 + Math.random() * 300,  // frames
    born: true
  };
}

particle = createParticle();

function drawParticle(p) {
  ctx.lineWidth = 0.2;
  ctx.strokeStyle = `rgba(255, 255, 255, ${p.opacity})`;
  ctx.beginPath();
  ctx.moveTo(p.x, p.y);

  if (p.type === 'spiral') {
    const spiralSteps = 8400;
    for (let i = 0; i < spiralSteps; i++) {
      let angle = p.angleOffset + i * 166.5;
      let radius = i * 1;
      ctx.lineTo(p.x + Math.cos(angle) * radius, p.y + Math.sin(angle) * radius);
    }
    p.angleOffset += 0.09 * p.spiralDirection;
  }

  ctx.stroke();

  // Movimiento
  p.x += p.vx;
  p.y += p.vy;
  p.vx += (Math.random() - 0.5) * 0.1;
  p.vy += (Math.random() - 0.5) * 0.1;

  // Fade in/out
  if (p.life > 550) { // Primeros 50 frames: FADE IN
    p.opacity += 0.01;
    if (p.opacity > p.baseOpacity) p.opacity = p.baseOpacity;
  } else if (p.life < 100) { // Últimos 100 frames: FADE OUT
    p.opacity -= 0.01;
    if (p.opacity < 0) p.opacity = 0;
  }

  p.life--;

  // Si termina la vida, crear nueva partícula
  if (p.life <= 0 || p.x < -100 || p.x > width + 100 || p.y < -100 || p.y > height + 100) {
    particle = createParticle();
  }
}

function drawNoise() {
  const imageData = ctx.getImageData(0, 0, width, height);
  const data = imageData.data;
  for (let i = 0; i < data.length; i += 4) {
    if (Math.random() < noiseDensity) {
      const glitchColor = Math.random() > 0.5 ? 255 : 0;
      data[i] = glitchColor;
      data[i+1] = glitchColor;
      data[i+2] = glitchColor;
      data[i+3] = 100;
    }
  }
  ctx.putImageData(imageData, 0, 0);
}

function drawHorizontalGlitch() {
  const sliceHeight = Math.floor(Math.random() * 20) + 5;
  const y = Math.floor(Math.random() * height);

  const slice = ctx.getImageData(0, y, width, sliceHeight);
  const offset = Math.floor(Math.random() * 40) - 20;
  ctx.putImageData(slice, offset, y);
}

function animate() {
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, width, height);

  drawParticle(particle);

  if (Math.random() < 0.8) drawHorizontalGlitch();
  if (Math.random() < 0.6) drawNoise();

  requestAnimationFrame(animate);
}

animate();
