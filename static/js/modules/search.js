export class SearchManager {
    constructor() {
        this.init();
    }

    init() {
        this.initSearchInputs();
    }

    initSearchInputs() {
        const searchInputs = document.querySelectorAll('input[type="search"], input[name="q"]');
        searchInputs.forEach(input => {
            let timeout;
            input.addEventListener('input', () => {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    if (input.value.length >= 3 || input.value.length === 0) {
                        input.closest('form').submit();
                    }
                }, 500);
            });
        });
    }
}

window.SearchManager = SearchManager;
