// ========================================
// MODERN PORTFOLIO JAVASCRIPT - DARK THEME
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('a[href^="#"]');

    // ========================================
    // SMOOTH SCROLLING - CENTER TITLE IN VIEWPORT
    // ========================================
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                // Special handling for contact section
                const isContactSection = targetId === '#contact';
                
                if (isContactSection) {
                    // For contact, position "Get In Touch" title just below navbar
                    const sectionTitle = targetSection.querySelector('.section-title');
                    if (sectionTitle) {
                        const titleTop = sectionTitle.getBoundingClientRect().top + window.pageYOffset;
                        // Position title about 120px from top (just below navbar)
                        const targetScroll = titleTop - 120;
                        
                        window.scrollTo({
                            top: targetScroll,
                            behavior: 'smooth'
                        });
                    } else {
                        // Fallback
                        window.scrollTo({
                            top: targetSection.offsetTop - 100,
                            behavior: 'smooth'
                        });
                    }
                } else {
                    // For other sections, center the title
                    setTimeout(() => {
                        const sectionTitle = targetSection.querySelector('.section-title');
                        
                        if (sectionTitle) {
                            // Get title's current position on page
                            const titleTop = sectionTitle.getBoundingClientRect().top + window.pageYOffset;
                            const titleHeight = sectionTitle.offsetHeight;
                            const windowHeight = window.innerHeight;
                            
                            // Calculate scroll position to center the title
                            const targetScroll = titleTop - (windowHeight / 2) + (titleHeight / 2);
                            
                            window.scrollTo({
                                top: targetScroll,
                                behavior: 'smooth'
                            });
                        } else {
                            // Fallback: just go to section start
                            window.scrollTo({
                                top: targetSection.offsetTop - 100,
                                behavior: 'smooth'
                            });
                        }
                    }, 50);
                }

                // Update active state immediately
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');

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
        
        if (scrolled > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ========================================
    // ACTIVE NAVIGATION HIGHLIGHTING
    // ========================================
    function updateActiveNav() {
        let current = '';
        const sections = document.querySelectorAll('section[id]');
        const scrollPosition = window.pageYOffset + 200; // Add offset for better detection
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        // Special handling for bottom of page (contact section)
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 100) {
            const lastSection = sections[sections.length - 1];
            current = lastSection.getAttribute('id');
        }
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href === `#${current}`) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveNav);
    // Initial call
    updateActiveNav();

    // ========================================
    // SCROLL REVEAL ANIMATION
    // ========================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.item-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // ========================================
    // AUTO-DISMISS ALERTS
    // ========================================
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // ========================================
    // PARALLAX EFFECT ON SCROLL - DISABLED (causes misalignment)
    // ========================================
    // Parallax effect disabled to prevent title misalignment

    // ========================================
    // TYPING EFFECT FOR HERO SECTION - DISABLED
    // ========================================
    // Typing effect disabled to show title immediately

    console.log('🚀 Portfolio Loaded - Dark Theme!');
});