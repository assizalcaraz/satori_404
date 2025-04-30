const canvas = document.getElementById('backgroundCanvas');
const ctx = canvas.getContext('2d');

let width, height;
function resizeCanvas() {
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

async function simularAgente(agente, contenedorId) {
  const res = await fetch('/interaccion/', { method: 'GET' });
  const data = await res.json();
  const rondas = data.interaccion?.ronda || [];

  const contenedor = document.getElementById(contenedorId);
  contenedor.innerHTML = '';  // Limpiamos para evitar duplicaciones

  rondas
    .filter(r => r.from.toLowerCase().includes(agente === 'arquitecto' ? 'a' : 'b'))
    .forEach(ronda => {
      const div = document.createElement('div');
      div.className = 'mensaje-ronda';

      const input = document.createElement('p');
      input.textContent = `🗣 ${ronda.input}`;

      const output = document.createElement('p');
      output.textContent = `💬 ${ronda.output}`;

      div.appendChild(input);
      div.appendChild(output);
      contenedor.appendChild(div);

      dibujarParticulaAleatoria(ronda.output.length);
    });
}

function dibujarParticulaAleatoria(fuerza) {
  ctx.beginPath();
  ctx.arc(Math.random() * width, Math.random() * height, fuerza * 0.4, 0, Math.PI * 2);
  ctx.fillStyle = `rgba(255, 0, 0, 0.15)`;
  ctx.fill();
}

setInterval(() => simularAgente('arquitecto', 'mensajes-arquitecto'), 8000);
setInterval(() => simularAgente('asistente', 'mensajes-asistente'), 12000);
