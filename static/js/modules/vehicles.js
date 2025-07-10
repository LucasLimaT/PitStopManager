export class VehiclesManager {
    constructor() {
        this.init();
    }

    init() {
        this.initReactivateOption();
    }

    initReactivateOption() {
        window.dismissReactivateOption = () => {
            const reactivateCard = document.querySelector('.card.border-warning');
            const vehicleForm = document.querySelector('#vehicleForm').closest('.modern-card');
            
            if (reactivateCard && vehicleForm) {
                reactivateCard.style.display = 'none';
                vehicleForm.style.opacity = '1';
                
                const firstInput = document.querySelector('#vehicleForm select, #vehicleForm input:not([type="hidden"])');
                if (firstInput) {
                    firstInput.focus();
                }
            }
        };
    }
}

window.VehiclesManager = VehiclesManager;
