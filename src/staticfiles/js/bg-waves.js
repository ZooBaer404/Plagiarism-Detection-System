// bg-waves.js — flowing waves left to right (slower)
(function () {
  const canvas = document.getElementById("bgCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let scale = 1;
  function resize() {
    scale = window.devicePixelRatio || 1;
    canvas.width = Math.floor(window.innerWidth * scale);
    canvas.height = Math.floor(window.innerHeight * scale);
    canvas.style.width = window.innerWidth + "px";
    canvas.style.height = window.innerHeight + "px";
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(scale, scale);
  }
  window.addEventListener("resize", resize);
  resize();

  let t = 0;

  function drawWave({ baseY, amp, freq, speed, color, phase }) {
    const w = window.innerWidth;
    const h = window.innerHeight;

    ctx.beginPath();
    ctx.moveTo(0, h);
    ctx.lineTo(0, baseY);

    for (let x = 0; x <= w; x++) {
      // ✅ add time to move waves left → right
      const y = baseY + Math.sin((x * freq) + (t * speed) + phase) * amp;
      ctx.lineTo(x, y);
    }

    ctx.lineTo(w, h);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width / scale, canvas.height / scale);

    drawWave({
      baseY: window.innerHeight * 0.65,
      amp: 60,
      freq: 0.02,
      speed: 0.02,   // slowed down
      color: "rgba(120, 200, 255, 0.35)",
      phase: 0,
    });

    drawWave({
      baseY: window.innerHeight * 0.7,
      amp: 50,
      freq: 0.018,
      speed: 0.015,  // slowed down
      color: "rgba(255, 140, 170, 0.25)",
      phase: 2,
    });

    t += 1;
    requestAnimationFrame(animate);
  }

  animate();
})();
