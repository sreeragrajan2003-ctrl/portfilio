// ========================================
// MODERN PORTFOLIO JAVASCRIPT - OPTIMIZED
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('a[href^="#"]');

    // ========================================
    // SMOOTH SCROLLING
    // ========================================
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                const navbarHeight = navbar.offsetHeight;
                const targetPosition = targetSection.offsetTop - navbarHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                // Close mobile menu if open
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            }
        });
    });

    // ========================================
    // NAVBAR SCROLL EFFECT
    // ========================================
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        
        if (scrolled > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.12)';
            navbar.style.boxShadow = '0 8px 32px rgba(0, 212, 255, 0.3)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.08)';
            navbar.style.boxShadow = '0 8px 32px rgba(0, 212, 255, 0.2)';
        }
    });

    // ========================================
    // ACTIVE NAVIGATION HIGHLIGHTING
    // ========================================
    window.addEventListener('scroll', function() {
        let current = '';
        const sections = document.querySelectorAll('section[id]');
        const navbarHeight = navbar.offsetHeight;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - navbarHeight - 100;
            const sectionHeight = section.clientHeight;
            
            if (pageYOffset >= sectionTop && pageYOffset < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    // ========================================
    // CARD ANIMATION ON SCROLL (DISABLED - Causing visibility issues)
    // ========================================
    // Cards are now always visible without animation

    // ========================================
    // FLOATING ORBS
    // ========================================
    function createFloatingOrbs() {
        const orbContainer = document.createElement('div');
        orbContainer.style.cssText = `
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
            pointer-events: none;
        `;

        for (let i = 0; i < 3; i++) {
            const orb = document.createElement('div');
            orb.style.cssText = `
                position: absolute;
                width: ${150 + Math.random() * 150}px;
                height: ${150 + Math.random() * 150}px;
                background: radial-gradient(circle, ${i % 2 === 0 ? '#00d4ff' : '#0066ff'} 0%, transparent 70%);
                border-radius: 50%;
                filter: blur(60px);
                opacity: 0.2;
                top: ${Math.random() * 100}%;
                left: ${Math.random() * 100}%;
                animation: float${i + 3} ${20 + Math.random() * 10}s infinite;
            `;
            orbContainer.appendChild(orb);
        }

        document.body.appendChild(orbContainer);
    }

    // Add orb animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float3 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(-80px, 60px) scale(1.2); }
            66% { transform: translate(60px, -80px) scale(0.8); }
        }
        @keyframes float4 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(50px, 80px) scale(1.15); }
        }
        @keyframes float5 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(70px, -40px) scale(0.9); }
            75% { transform: translate(-60px, 70px) scale(1.1); }
        }
    `;
    document.head.appendChild(style);

    createFloatingOrbs();

    // ========================================
    // AUTO-DISMISS ALERTS
    // ========================================
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    console.log('🚀 Portfolio Loaded!');
});