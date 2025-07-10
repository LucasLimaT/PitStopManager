import { TooltipsManager } from './modules/tooltips.js';
import { AlertsManager } from './modules/alerts.js';
import { FormsManager } from './modules/forms.js';
import { SearchManager } from './modules/search.js';
import { FormattingManager } from './modules/formatting.js';
import { NavbarManager } from './modules/navbar.js';
import { UtilsManager } from './modules/utils.js';
import { VehiclesManager } from './modules/vehicles.js';
import { KebabMenuManager } from './modules/kebab-menu.js';

document.addEventListener('DOMContentLoaded', function() {
    
    new TooltipsManager();
    new AlertsManager();
    new FormsManager();
    new SearchManager();
    new FormattingManager();
    new NavbarManager();
    new VehiclesManager();
    new KebabMenuManager();
    
    UtilsManager.initYearObserver();
});


window.PitStopManager = {
    formatCurrency: FormattingManager.formatCurrency,
    formatDate: FormattingManager.formatDate,
    formatDateTime: FormattingManager.formatDateTime,
    showLoading: UtilsManager.showLoading,
    hideLoading: UtilsManager.hideLoading,
    showNotification: AlertsManager.showNotification,
    makeAjaxRequest: UtilsManager.makeAjaxRequest
};
