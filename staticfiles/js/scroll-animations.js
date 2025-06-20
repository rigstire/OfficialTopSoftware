// Scroll Animation System
class ScrollAnimations {
    constructor() {
        this.init();
    }

    init() {
        // Create intersection observer
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Observe all elements with animation classes
        this.observeElements();
        
        // Add parallax effect to hero sections
        this.initParallax();
        
        // Add counter animations
        this.initCounters();
    }

    observeElements() {
        const animatedElements = document.querySelectorAll(
            '.fade-in, .slide-in-left, .slide-in-right, .slide-in-up, .slide-in-down, .zoom-in, .stagger-item'
        );
        
        animatedElements.forEach(el => {
            this.observer.observe(el);
        });
    }

    initParallax() {
        const parallaxElements = document.querySelectorAll('.parallax');
        
        if (parallaxElements.length > 0) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                
                parallaxElements.forEach(element => {
                    const speed = element.dataset.speed || 0.5;
                    const yPos = -(scrolled * speed);
                    element.style.transform = `translateY(${yPos}px)`;
                });
            });
        }
    }

    initCounters() {
        const counters = document.querySelectorAll('.counter');
        
        counters.forEach(counter => {
            const target = parseInt(counter.dataset.target);
            const duration = parseInt(counter.dataset.duration) || 2000;
            
            this.observer.observe(counter);
            
            counter.addEventListener('animationstart', () => {
                this.animateCounter(counter, target, duration);
            });
        });
    }

    animateCounter(element, target, duration) {
        let start = 0;
        const increment = target / (duration / 16);
        
        const timer = setInterval(() => {
            start += increment;
            element.textContent = Math.floor(start);
            
            if (start >= target) {
                element.textContent = target;
                clearInterval(timer);
            }
        }, 16);
    }

    // Method to add stagger effect to multiple elements
    static addStaggerEffect(selector, delay = 100) {
        const elements = document.querySelectorAll(selector);
        elements.forEach((el, index) => {
            el.style.animationDelay = `${index * delay}ms`;
            el.classList.add('stagger-item');
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ScrollAnimations();
    
    // Add stagger effects to specific elements
    ScrollAnimations.addStaggerEffect('.service-card', 150);
    ScrollAnimations.addStaggerEffect('.project-section', 200);
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}); 