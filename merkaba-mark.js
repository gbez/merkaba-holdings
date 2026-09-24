/* Merkaba Holdings — rotating mark.
   Usage: <script src="merkaba-mark.js"></script>
          <merkaba-mark size="160" theme="dark" echoes="6" speed="0.5"></merkaba-mark>
   Attributes: size (px), theme ("light" | "dark" background), echoes (0–6), speed (rad/s, 0 = static) */
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const V = [[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]];
  const TETS = [V, V.map(v => v.map(c => -c))];
  const F = [[0,1,2],[0,1,3],[0,2,3],[1,2,3]], E = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const L = [-0.4, 0.6, 0.7], LN = Math.hypot(...L);
  const rot = ([x,y,z], ry, rx) => {
    [x, z] = [x*Math.cos(ry) + z*Math.sin(ry), -x*Math.sin(ry) + z*Math.cos(ry)];
    [y, z] = [y*Math.cos(rx) - z*Math.sin(rx), y*Math.sin(rx) + z*Math.cos(rx)];
    return [x,y,z];
  };
  class MerkabaMark extends HTMLElement {
    static get observedAttributes() { return ['size','theme','echoes','speed']; }
    connectedCallback() {
      this.style.display = 'inline-block';
      this.svg = document.createElementNS(NS, 'svg');
      this.svg.style.overflow = 'visible';
      this.appendChild(this.svg);
      this.t = 0; let last = performance.now();
      const tick = now => {
        this.t += (now - last) / 1000 * this.speed; last = now;
        this.draw(); this.raf = requestAnimationFrame(tick);
      };
      this.raf = requestAnimationFrame(tick);
    }
    disconnectedCallback() { cancelAnimationFrame(this.raf); }
    get speed() { return parseFloat(this.getAttribute('speed') ?? '0.5'); }
    draw() {
      const size = parseFloat(this.getAttribute('size') ?? '160');
      const dark = (this.getAttribute('theme') ?? 'dark') === 'dark';
      const echoes = parseInt(this.getAttribute('echoes') ?? '6', 10);
      const t = this.t, c = size / 2, ink = dark ? '#f3ede4' : '#3b2e24';
      const proj = (p, s) => [c + p[0]*s, c - p[1]*s];
      let out = '';
      for (let k = echoes; k >= 1; k--) {
        const s = size * 0.27 * (1 + k * 0.1), ry = t + 0.25 - k * 0.22;
        TETS.forEach((tet, ti) => {
          const P = tet.map(v => proj(rot(v, ry, 0.95 - k * 0.05), s));
          const col = `oklch(0.68 0.16 ${(ti ? 330 : 60) - k * 35})`;
          E.forEach(([a,b]) => out += `<line x1="${P[a][0]}" y1="${P[a][1]}" x2="${P[b][0]}" y2="${P[b][1]}" stroke="${col}" stroke-width="${Math.max(1, size/70)}" opacity="${Math.max(0.05, 0.85 - k*0.15)}"/>`);
        });
      }
      const faces = [];
      TETS.forEach((tet, ti) => {
        const R = tet.map(v => rot(v, t + 0.25, 0.95));
        F.forEach((f, fi) => {
          const [a,b,cc] = f.map(i => R[i]);
          const u = b.map((v,i) => v - a[i]), w = cc.map((v,i) => v - a[i]);
          let n = [u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0]];
          const cen = [0,1,2].map(i => (a[i]+b[i]+cc[i])/3);
          if (n[0]*cen[0]+n[1]*cen[1]+n[2]*cen[2] < 0) n = n.map(v => -v);
          const lit = Math.max(0, (n[0]*L[0]+n[1]*L[1]+n[2]*L[2]) / Math.hypot(...n) / LN);
          const hue = ti ? 330 - fi*18 : 45 + fi*14;
          faces.push({ z: cen[2], pts: f.map(i => proj(R[i], size*0.27).join(',')).join(' '), fill: `oklch(${(0.5+0.35*lit).toFixed(3)} 0.15 ${hue} / 0.6)` });
        });
      });
      faces.sort((a,b) => a.z - b.z).forEach(f => out += `<polygon points="${f.pts}" fill="${f.fill}" stroke="${ink}" stroke-width="${Math.max(0.8, size/70)}" stroke-linejoin="round" style="mix-blend-mode:${dark ? 'screen' : 'multiply'}"/>`);
      this.svg.setAttribute('width', size); this.svg.setAttribute('height', size);
      this.svg.setAttribute('viewBox', `0 0 ${size} ${size}`);
      this.svg.innerHTML = out;
    }
  }
  customElements.define('merkaba-mark', MerkabaMark);
})();
