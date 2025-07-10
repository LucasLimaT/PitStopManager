export class UtilsManager {
    
    static showLoading(element) {
        if (element) {
            element.innerHTML = '<span class="spinner"></span> Carregando...';
            element.disabled = true;
        }
    }

    static hideLoading(element, originalText) {
        if (element) {
            element.innerHTML = originalText;
            element.disabled = false;
        }
    }

    static getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    static makeAjaxRequest(url, options = {}) {
        const defaults = {
            headers: {
                'X-CSRFToken': UtilsManager.getCSRFToken(),
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        };
        
        return fetch(url, { ...defaults, ...options });
    }

    static initYearObserver() {
        const yearInputs = document.querySelectorAll('input[name*="ano"], input[name*="year"]');
        
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'value') {
                    const target = mutation.target;
                    if (target?.matches?.('input[name*="ano"], input[name*="year"]')) {
                        const value = target.value.toString().replace(/[^\d]/g, '');
                        if (value !== target.value) {
                            target.value = value.substring(0, 4);
                        }
                    }
                }
            });
        });

        yearInputs.forEach(input => {
            observer.observe(input, { attributes: true, attributeFilter: ['value'] });
        });

        return observer;
    }
}


window.UtilsManager = UtilsManager;
