export class FormsManager {
    constructor() {
        this.init();
    }

    init() {
        this.initFormValidation();
        this.initDateConstraints();
        this.initFocusManagement();
        this.initSpecificForms();
    }

    initFormValidation() {
        const forms = document.querySelectorAll('form[novalidate]');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }

    initDateConstraints() {
        const dataEntradaInput = document.getElementById('id_data_de_entrada');
        const dataEntregaInput = document.getElementById('id_data_de_entrega');

        if (dataEntradaInput && dataEntregaInput) {
            dataEntradaInput.addEventListener('change', () => {
                dataEntregaInput.min = dataEntradaInput.value;
            });

            if (dataEntradaInput.value) {
                dataEntregaInput.min = dataEntradaInput.value;
            }
        }
    }

    initFocusManagement() {
        if (!document.querySelector('.card.border-warning')) {
            const firstInput = document.querySelector('#vehicleForm select, #vehicleForm input:not([type="hidden"])');
            if (firstInput) {
                firstInput.focus();
            }
        }
    }

    initSpecificForms() {
        if (document.querySelector('[data-form-type="product"]')) {
            this.initProductForm();
        }

        if (document.querySelector('[data-form-type="appointment"]')) {
            this.initAppointmentForm();
        }

        if (document.querySelector('[data-form-type="service"]')) {
            this.initServiceForm();
        }

        if (document.querySelector('[data-form-type="vehicle"]')) {
            this.initVehicleForm();
        }
    }

    initProductForm() {
        const firstInput = document.querySelector('input[name="nome"]');
        if (firstInput) {
            firstInput.focus();
        }
    }

    initAppointmentForm() {
        const dateTimeInput = document.querySelector('input[name="data_do_agendamento"]');
        if (dateTimeInput) {
            const now = new Date();
            const year = now.getFullYear();
            const month = (now.getMonth() + 1).toString().padStart(2, '0');
            const day = now.getDate().toString().padStart(2, '0');
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            
            const minDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
            dateTimeInput.min = minDateTime;

            const isCreateForm = dateTimeInput.dataset.isCreateForm === 'true';

            if (isCreateForm && !dateTimeInput.value) {
                const defaultDate = new Date(now.getTime() + 60 * 60 * 1000); 
                const defaultYear = defaultDate.getFullYear();
                const defaultMonth = (defaultDate.getMonth() + 1).toString().padStart(2, '0');
                const defaultDay = defaultDate.getDate().toString().padStart(2, '0');
                const defaultHours = defaultDate.getHours().toString().padStart(2, '0');
                const defaultMinutes = defaultDate.getMinutes().toString().padStart(2, '0');
                dateTimeInput.value = `${defaultYear}-${defaultMonth}-${defaultDay}T${defaultHours}:${defaultMinutes}`;
            }
        }

        const firstSelect = document.querySelector('select, input:not([type="hidden"])');
        if (firstSelect) {
            firstSelect.focus();
        }
    }

    initServiceForm() {
        const dateInput = document.querySelector('input[type="date"]');
        if (dateInput && !dateInput.valueAsDate) {
            
        }
    }

    initVehicleForm() {
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

window.FormsManager = FormsManager;
