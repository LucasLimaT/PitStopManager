export class FormattingManager {
    constructor() {
        this.init();
    }

    init() {
        this.initPhoneFormatting();
        this.initPlateFormatting();
        this.initYearInputs();
        this.initNumberFormatting();
        this.initStockInputs();
    }

    initPhoneFormatting() {
        const phoneInputs = document.querySelectorAll('input[name*="phone"], input[name*="telefone"]');
        phoneInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length <= 11) {
                    if (value.length <= 10) {
                        value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
                    } else {
                        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
                    }
                }
                e.target.value = value;
            });
        });
    }

    initPlateFormatting() {
        const plateInputs = document.querySelectorAll('input[name*="plate"], input[name*="placa"]');
        plateInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                let value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
                
                if (value.length <= 7) {
                    if (value.length > 3) {
                        value = value.replace(/(\w{3})(\w+)/, '$1-$2');
                    }
                }
                
                e.target.value = value;
            });
        });

        const placaInput = document.getElementById('id_placa');
        if (placaInput) {
            placaInput.addEventListener('input', (e) => {
                let value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
                if (value.length > 7 && value.indexOf('-') === -1) {
                    
                } else if (value.length > 3 && value.indexOf('-') === -1 && /^[A-Z]{3}$/.test(value.substr(0,3)) && /^\d.*/.test(value.substr(3))) {
                    value = value.substr(0,3) + '-' + value.substr(3);
                }
                if (value.length > 8) {
                    value = value.substr(0,8);
                }
                e.target.value = value;
            });
        }
    }

    initYearInputs() {
        const yearInputs = document.querySelectorAll('input[name*="ano"], input[name*="year"]');
        yearInputs.forEach(input => {
            input.setAttribute('inputmode', 'numeric');
            input.setAttribute('pattern', '[0-9]*');
            input.setAttribute('maxlength', '4');
            input.setAttribute('min', '1900');
            input.setAttribute('max', new Date().getFullYear() + 1);
            input.setAttribute('step', '1');
            
            const cleanYearValue = (value) => {
                let cleanValue = value.toString().replace(/[^\d]/g, '');
                if (cleanValue.length > 4) {
                    cleanValue = cleanValue.substring(0, 4);
                }
                return cleanValue;
            };
            
            input.addEventListener('input', (e) => {
                const cleanValue = cleanYearValue(e.target.value);
                e.target.value = cleanValue;
            });
            
            input.addEventListener('blur', (e) => {
                const cleanValue = cleanYearValue(e.target.value);
                e.target.value = cleanValue;
            });
            
            input.addEventListener('focus', (e) => {
                const cleanValue = cleanYearValue(e.target.value);
                e.target.value = cleanValue;
            });
            
            input.addEventListener('keydown', (e) => {
                if ([46, 8, 9, 27, 13].indexOf(e.keyCode) !== -1 ||
                    (e.keyCode === 65 && e.ctrlKey === true) ||
                    (e.keyCode === 67 && e.ctrlKey === true) ||
                    (e.keyCode === 86 && e.ctrlKey === true) ||
                    (e.keyCode === 88 && e.ctrlKey === true) ||
                    (e.keyCode >= 35 && e.keyCode <= 39)) {
                    
                    if (e.keyCode === 110 || e.keyCode === 190 || e.keyCode === 188) {
                        e.preventDefault();
                    }
                    return;
                }
                if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                    e.preventDefault();
                }
            });
            
            input.addEventListener('paste', (e) => {
                e.preventDefault();
                const paste = (e.clipboardData || window.clipboardData).getData('text');
                const cleanValue = cleanYearValue(paste);
                if (cleanValue) {
                    e.target.value = cleanValue;
                    e.target.dispatchEvent(new Event('input', { bubbles: true }));
                }
            });
            
            if (input.value) {
                input.value = cleanYearValue(input.value);
            }
        });

        const anoInput = document.getElementById('id_ano');
        if (anoInput) {
            anoInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 4) {
                    value = value.substring(0, 4);
                }
                e.target.value = value;
            });
        }

        document.addEventListener('focusout', (e) => {
            if (e.target.matches('input[name*="ano"], input[name*="year"]')) {
                let value = e.target.value.toString();
                value = value.replace(/[^\d]/g, '');
                if (value.length > 4) {
                    value = value.substring(0, 4);
                }
                e.target.value = value;
            }
        });
    }

    initNumberFormatting() {
        const numberInputs = document.querySelectorAll('input[type="number"], .number-format');
        numberInputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.value) {
                    const value = parseFloat(this.value);
                    if (!isNaN(value)) {
                        this.value = value.toFixed(2);
                    }
                }
            });
        });
    }

    initStockInputs() {
        const stockInputs = document.querySelectorAll('input[name*="estoque"], input[name*="stock"], input[name*="quantity"]');
        stockInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                let value = e.target.value.replace(/[^\d]/g, '');
                e.target.value = value;
            });
            
            input.addEventListener('keydown', (e) => {
                if ([46, 8, 9, 27, 13].indexOf(e.keyCode) !== -1 ||
                    (e.keyCode === 65 && e.ctrlKey === true) ||
                    (e.keyCode === 67 && e.ctrlKey === true) ||
                    (e.keyCode === 86 && e.ctrlKey === true) ||
                    (e.keyCode === 88 && e.ctrlKey === true) ||
                    (e.keyCode >= 35 && e.keyCode <= 39)) {
                    return;
                }
                if (e.keyCode === 110 || e.keyCode === 190 || e.keyCode === 188) {
                    e.preventDefault();
                    return;
                }
                if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                    e.preventDefault();
                }
            });
        });
    }

    static formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }

    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR');
    }

    static formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('pt-BR');
    }
}


window.FormattingManager = FormattingManager;
