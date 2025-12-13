// ========================================
// MODERN PORTFOLIO JAVASCRIPT
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // HIDE ONLY EMPTY CARDS (NOT SECTIONS)
    // ========================================
    function hideEmptyCards() {
        // Hide empty card columns only
        document.querySelectorAll('.col-lg-4, .col-md-6').forEach(col => {
            const card = col.querySelector('.item-card');
            if (card) {
                const cardBody = card.querySelector('.card-body');
                
                // Check if card has any meaningful content
                const hasIcon = cardBody && cardBody.querySelector('.item-icon i');
                const hasTitle = cardBody && cardBody.querySelector('.card-title')?.textContent.trim();
                const hasSubtitle = cardBody && cardBody.querySelector('.card-subtitle')?.textContent.trim();
                const hasDescription = cardBody && cardBody.querySelector('.card-text')?.textContent.trim();
                const hasOtherContent = cardBody && Array.from(cardBody.querySelectorAll('p')).some(p => {
                    return p.textContent.trim() && !p.classList.contains('card-text');
                });
                
                // Hide card only if it has absolutely no content
                if (!hasIcon && !hasTitle && !hasSubtitle && !hasDescription && !hasOtherContent) {
                    col.style.display = 'none';
                }
            }
        });

        // If a section has no visible cards, hide only the card grid container, not the whole section
        document.querySelectorAll('section[id]').forEach(section => {
            if (section.id === 'home' || section.id === 'contact') return;
            
            const cardGrid = section.querySelector('.row.g-4');
            if (cardGrid) {
                const visibleCards = Array.from(cardGrid.querySelectorAll('.col-lg-4, .col-md-6')).filter(col => {
                    return col.style.display !== 'none';
                });
                
                // If no visible cards, hide only the card grid, keep section title and description visible
                if (visibleCards.length === 0) {
                    cardGrid.style.display = 'none';
                }
            }
        });
    }

    hideEmptyCards();

    // ========================================
    // SMOOTH SCROLLING
    // ========================================
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
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
    // NAVBAR SCROLL EFFECTS
    // ========================================
    let lastScroll = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.12)';
            navbar.style.boxShadow = '0 8px 32px rgba(0, 212, 255, 0.3)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.08)';
            navbar.style.boxShadow = '0 8px 32px rgba(0, 212, 255, 0.2)';
        }
        
        lastScroll = currentScroll;
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
    // CARD SCROLL ANIMATIONS
    // ========================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(30px)';
                
                setTimeout(() => {
                    entry.target.style.transition = 'all 0.6s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all visible cards
    const cards = document.querySelectorAll('.item-card');
    cards.forEach((card, index) => {
        const col = card.closest('.col-lg-4, .col-md-6');
        if (col && col.style.display !== 'none') {
            card.style.transitionDelay = `${index * 0.1}s`;
            observer.observe(card);
        }
    });

    // ========================================
    // FORM SUBMISSION ANIMATION
    // ========================================
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            submitBtn.disabled = true;
            
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }

    // ========================================
    // PARALLAX HERO EFFECT
    // ========================================
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;
            heroSection.style.transform = `translateY(${parallax}px)`;
        });
    }

    // ========================================
    // SCROLL INDICATOR
    // ========================================
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', function() {
            const sections = document.querySelectorAll('section[id]');
            let firstVisibleSection = null;
            
            for (let section of sections) {
                if (section.id !== 'home') {
                    firstVisibleSection = section;
                    break;
                }
            }
            
            if (firstVisibleSection) {
                firstVisibleSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // ========================================
    // FLOATING ORBS
    // ========================================
    function createFloatingOrbs() {
        const orbContainer = document.createElement('div');
        orbContainer.className = 'floating-orbs';
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
                animation: float${i + 2} ${20 + Math.random() * 10}s infinite;
            `;
            orbContainer.appendChild(orb);
        }

        document.body.appendChild(orbContainer);
    }

    const style = document.createElement('style');
    style.textContent = `
        @keyframes float2 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(-80px, 60px) scale(1.2); }
            66% { transform: translate(60px, -80px) scale(0.8); }
        }
        @keyframes float3 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(50px, 80px) scale(1.15); }
        }
        @keyframes float4 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(70px, -40px) scale(0.9); }
            75% { transform: translate(-60px, 70px) scale(1.1); }
        }
    `;
    document.head.appendChild(style);

    createFloatingOrbs();

    // ========================================
    // BUTTON GLOW EFFECTS
    // ========================================
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.filter = 'brightness(1.2)';
        });
        button.addEventListener('mouseleave', function() {
            this.style.filter = 'brightness(1)';
        });
    });

    // ========================================
    // AUTO-DISMISS ALERTS
    // ========================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    console.log('🚀 Modern Portfolio Loaded Successfully!');
});