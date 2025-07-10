function toggleKebabMenu(button) {
    const dropdown = button.nextElementSibling;
    const isOpen = dropdown.classList.contains('show');
    document.querySelectorAll('.kebab-dropdown.show').forEach(d => {
        d.classList.remove('show');
    });
    if (!isOpen) {
        dropdown.classList.add('show');
    }
}

document.addEventListener('click', function(event) {
    if (!event.target.closest('.kebab-menu')) {
        document.querySelectorAll('.kebab-dropdown.show').forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    }
});

export class KebabMenuManager {
    constructor() {
        this.init();
    }
    init() {
        this.bindEvents();
        this.setupClickOutside();
    }
    bindEvents() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.kebab-btn')) {
                e.preventDefault();
                e.stopPropagation();
                this.toggleKebabMenu(e.target.closest('.kebab-btn'));
            }
        });
    }
    setupClickOutside() {
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.kebab-menu')) {
                this.closeAllMenus();
            }
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllMenus();
            }
        });
    }
    toggleKebabMenu(button) {
        const menu = button.closest('.kebab-menu');
        const dropdown = menu.querySelector('.kebab-dropdown');
        this.closeAllMenus();
        if (dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        } else {
            dropdown.classList.add('show');
            this.adjustMenuPosition(dropdown);
        }
    }
    closeAllMenus() {
        const openMenus = document.querySelectorAll('.kebab-dropdown.show');
        openMenus.forEach(menu => {
            menu.classList.remove('show');
        });
    }
    adjustMenuPosition(dropdown) {
        dropdown.style.top = '';
        dropdown.style.bottom = '';
        dropdown.style.left = '';
        dropdown.style.right = '';
        dropdown.style.marginTop = '';
        dropdown.style.marginBottom = '';
        const rect = dropdown.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const windowWidth = window.innerWidth;
        if (rect.bottom > windowHeight) {
            dropdown.style.top = 'auto';
            dropdown.style.bottom = '100%';
            dropdown.style.marginBottom = '4px';
        } else {
            dropdown.style.top = '100%';
            dropdown.style.marginTop = '4px';
        }
        if (rect.right > windowWidth) {
            dropdown.style.right = '0';
            dropdown.style.left = 'auto';
        }
        if (rect.left < 0) {
            dropdown.style.left = '0';
            dropdown.style.right = 'auto';
        }
    }
}

document.addEventListener('click', (e) => {
    if (!e.target.closest('.kebab-menu')) {
        const openMenus = document.querySelectorAll('.kebab-dropdown.show');
        openMenus.forEach(menu => {
            menu.classList.remove('show');
        });
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const openMenus = document.querySelectorAll('.kebab-dropdown.show');
        openMenus.forEach(menu => {
            menu.classList.remove('show');
        });
    }
});

window.toggleKebabMenu = function(button) {
    const menu = button.closest('.kebab-menu');
    const dropdown = menu.querySelector('.kebab-dropdown');
    const openMenus = document.querySelectorAll('.kebab-dropdown.show');
    openMenus.forEach(openMenu => {
        if (openMenu !== dropdown) {
            openMenu.classList.remove('show');
        }
    });
    if (dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
    } else {
        dropdown.classList.add('show');
        requestAnimationFrame(() => {
            const rect = dropdown.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            const windowWidth = window.innerWidth;
            const table = button.closest('table');
            const row = button.closest('tr');
            let isNearBottom = false;
            if (table && row) {
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                const currentRowIndex = rows.indexOf(row);
                const totalRows = rows.length;
                isNearBottom = currentRowIndex >= totalRows - 2 || rect.bottom > windowHeight - 20;
            } else {
                isNearBottom = rect.bottom > windowHeight - 20;
            }
            dropdown.style.top = '';
            dropdown.style.bottom = '';
            dropdown.style.left = '';
            dropdown.style.right = '';
            dropdown.style.marginTop = '';
            dropdown.style.marginBottom = '';
            if (isNearBottom) {
                dropdown.style.top = 'auto';
                dropdown.style.bottom = '100%';
                dropdown.style.marginBottom = '4px';
            } else {
                dropdown.style.top = '100%';
                dropdown.style.marginTop = '4px';
            }
            if (rect.right > windowWidth - 20) {
                dropdown.style.right = '0';
                dropdown.style.left = 'auto';
            } else if (rect.left < 20) {
                dropdown.style.left = '0';
                dropdown.style.right = 'auto';
            }
        });
    }
};
