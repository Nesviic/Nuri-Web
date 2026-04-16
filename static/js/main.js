// JS/main.js
document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. LÓGICA DEL MENÚ MÓVIL (HAMBURGUESA) ---
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileBtn && mobileMenu) {
        const icon = mobileBtn.querySelector('.material-symbols-outlined');

        mobileBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            if (mobileMenu.classList.contains('hidden')) {
                icon.textContent = 'menu';
                icon.style.transform = 'rotate(0deg)';
            } else {
                icon.textContent = 'close';
                icon.style.transform = 'rotate(90deg)';
            }
        });
    }

    // --- 2. LÓGICA DE PÁGINA ACTIVA AUTOMÁTICA ---
    let currentPath = window.location.pathname.split('/').pop();
    if (currentPath === '') currentPath = 'index.html';

    const navLinks = document.querySelectorAll('.nav-link');
    
    // Clases exactas de Tailwind para el estado ACTIVO
    const activeClasses = ['text-[#516356]', 'dark:text-[#d4e7d8]', 'font-bold', 'border-b-2', 'border-[#516356]', 'dark:border-[#d4e7d8]', 'pb-1'];
    
    // Clases para el estado INACTIVO
    const inactiveClasses = ['text-[#31332c]/60', 'dark:text-[#fbf9f4]/60', 'hover:opacity-80'];

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Limpiamos clases previas por si acaso
        link.classList.remove(...activeClasses, ...inactiveClasses);

        if (href === currentPath) {
            // Si el link coincide con la página actual, lo encendemos
            link.classList.add(...activeClasses);
        } else {
            // Si no, lo apagamos
            link.classList.add(...inactiveClasses);
        }
    });
});