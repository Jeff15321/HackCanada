import React, { useEffect, useRef } from 'react';

interface ParticlesProps {
  isActive: boolean;
  color?: string;
}

const Particles: React.FC<ParticlesProps> = ({ isActive, color = '#6ee7b7' }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particles = useRef<any[]>([]);

  useEffect(() => {
    if (!isActive) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    class Particle {
      x: number;
      y: number;
      size: number;
      speedX: number;
      speedY: number;
      alpha: number;
      initialSize: number;
      lifespan: number;
      currentLife: number;

      constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
        this.initialSize = Math.random() * 10 + 8;
        this.size = this.initialSize;
        this.speedX = Math.random() * 6 - 3;
        this.speedY = Math.random() * 6 - 3;
        this.alpha = 1;
        this.lifespan = 100;
        this.currentLife = 0;
      }

      update() {
        this.currentLife++;
        const lifeProgress = this.currentLife / this.lifespan;
        
        this.x += this.speedX;
        this.y += this.speedY;
        
        this.size = Math.max(1, this.initialSize * (1 - lifeProgress));
        this.alpha = 1 - lifeProgress;
      }

      isDead() {
        return this.currentLife >= this.lifespan;
      }

      draw(ctx: CanvasRenderingContext2D, color: string) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        const alpha = Math.floor(this.alpha * 255).toString(16).padStart(2, '0');
        ctx.fillStyle = `${color}${alpha}`;
        ctx.fill();
      }
    }

    const createParticles = (x: number, y: number) => {
      // Create more particles on click
      for (let i = 0; i < 50; i++) {
        particles.current.push(new Particle(x, y));
      }
    };

    const animate = () => {
      if (!ctx || !isActive) return;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.current = particles.current.filter(particle => !particle.isDead());

      particles.current.forEach(particle => {
        particle.update();
        particle.draw(ctx, color);
      });

      requestAnimationFrame(animate);
    };

    const handleClick = (e: MouseEvent) => {
      createParticles(e.clientX, e.clientY);
    };

    window.addEventListener('click', handleClick);
    animate();

    return () => {
      window.removeEventListener('click', handleClick);
    };
  }, [isActive, color]);

  if (!isActive) return null;

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-[9999]"
    />
  );
};

export default Particles; 