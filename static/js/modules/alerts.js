export class AlertsManager {
    constructor() {
        this.init();
    }

    init() {
        this.initAutoHideAlerts();
        this.initDeleteConfirmations();
        this.initMessageAlerts();
    }

    initAutoHideAlerts() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }

    initDeleteConfirmations() {
        const deleteButtons = document.querySelectorAll('a[href*="delete"], button[data-action="delete"]');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                if (!confirm('Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.')) {
                    e.preventDefault();
                    return false;
                }
            });
        });
    }

    initMessageAlerts() {
        const messageCloseButtons = document.querySelectorAll('.modern-alert-close');
        messageCloseButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.target.closest('.modern-alert').style.display = 'none';
            });
        });
    }

    static showNotification(message, type = 'success') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container') || document.body;
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

window.AlertsManager = AlertsManager;
