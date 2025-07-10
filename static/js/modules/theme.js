export class ThemeManager {
    constructor() {
        this.init();
    }

    init() {
        
        console.log('Theme Manager initialized');
    }

    
    static setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }

    static getTheme() {
        return localStorage.getItem('theme') || 'light';
    }
}


window.ThemeManager = ThemeManager;
