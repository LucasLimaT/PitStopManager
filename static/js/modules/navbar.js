export class NavbarManager {
    constructor() {
        this.init();
    }

    init() {
        this.initScrollBehavior();
    }

    initScrollBehavior() {
        let lastScrollTop = 0;
        const navbar = document.querySelector('.modern-header');
        const scrollThreshold = 50; 
        
        const handleNavbarScroll = () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (Math.abs(scrollTop - lastScrollTop) < scrollThreshold) {
                return;
            }
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                navbar.classList.add('navbar-hidden');
            } else {
                navbar.classList.remove('navbar-hidden');
            }
            
            lastScrollTop = scrollTop;
        };
        
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    handleNavbarScroll();
                    ticking = false;
                });
                ticking = true;
            }
        });
    }
}


window.NavbarManager = NavbarManager;
