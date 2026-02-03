let scene, camera, renderer, particles, mainNode;

function init() {
    const canvas = document.getElementById('three-canvas');
    if (!canvas) return;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 6;

    renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);

    const pGeo = new THREE.BufferGeometry();
    const pos = [];
    const cols = [];
    for(let i = 0; i < 4000; i++) {
        pos.push(THREE.MathUtils.randFloatSpread(30), THREE.MathUtils.randFloatSpread(30), THREE.MathUtils.randFloatSpread(30));
        cols.push(0, 0.27, 1);
    }
    pGeo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    pGeo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
    
    particles = new THREE.Points(pGeo, new THREE.PointsMaterial({ size: 0.03, vertexColors: true, transparent: true, opacity: 0.5 }));
    scene.add(particles);

    const geometry = new THREE.IcosahedronGeometry(2, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.1 });
    mainNode = new THREE.Mesh(geometry, material);
    scene.add(mainNode);

    animate();
}

function animate() {
    requestAnimationFrame(animate);
    particles.rotation.y += 0.001;
    mainNode.rotation.x += 0.005;
    mainNode.rotation.y += 0.005;
    renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// === MODAL LOGIC ===
window.openAuthModal = () => {
    const modal = document.getElementById('auth-modal');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
};

window.closeAuthModal = () => {
    const modal = document.getElementById('auth-modal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
};

init();