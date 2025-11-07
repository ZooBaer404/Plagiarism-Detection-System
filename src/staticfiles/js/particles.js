// PS5-style flowing wave background
const canvas = document.getElementById("bgCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let waveOffset = 0;

function drawWave(color, amplitude, wavelength, speed, yOffset) {
  ctx.beginPath();
  ctx.moveTo(0, canvas.height / 2);

  for (let x = 0; x <= canvas.width; x++) {
    const y =
      amplitude * Math.sin((x / wavelength) + waveOffset * speed) +
      canvas.height / 2 +
      yOffsaet;
    ctx.lineTo(x, y);
  }

  ctx.lineTo(canvas.width, canvas.height);
  ctx.lineTo(0, canvas.height);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Brighter, more visible waves
  // PS5-style flowing wave background
const canvas = document.getElementById("bgCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let waveOffset = 0;

function drawWave(color, amplitude, wavelength, speed, yOffset) {
  ctx.beginPath();
  ctx.moveTo(0, canvas.height / 2);

  for (let x = 0; x <= canvas.width; x++) {
    const y =
      amplitude * Math.sin((x / wavelength) + waveOffset * speed) +
      canvas.height / 2 +
      yOffset;
    ctx.lineTo(x, y);
  }

  ctx.lineTo(canvas.width, canvas.height);
  ctx.lineTo(0, canvas.height);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Brighter, more visible waves
  drawWave("rgba(173, 216, 230, 0.6)", 40, 280, 0.6, 0);   // light blue
  drawWave("rgba(135, 206, 250, 0.5)", 60, 420, 0.4, 25);  // sky blue
  drawWave("rgba(255, 182, 193, 0.4)", 80, 500, 0.2, -30); // pale pink/red

  waveOffset += 0.02;
  requestAnimationFrame(animate);
}

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

animate();

  waveOffset += 0.02;
  requestAnimationFrame(animate);
}

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

animate();
