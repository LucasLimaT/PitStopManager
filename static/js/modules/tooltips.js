export class TooltipsManager {
    constructor() {
        this.init();
    }

    init() {
        this.initTooltips();
        this.initPopovers();
    }

    initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    initPopovers() {
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(popoverTriggerEl => {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }
}

window.TooltipsManager = TooltipsManager;
