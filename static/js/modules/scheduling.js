export class SchedulingManager {
    constructor() {
        this.appointmentsData = [];
        this.init();
    }

    init() {
        this.initAppointmentsList();
    }

    initAppointmentsList() {
        const appointmentsList = document.querySelector('[data-appointments-json]');
        if (appointmentsList) {
            try {
                const appointmentsJson = appointmentsList.dataset.appointmentsJson;
                this.appointmentsData = JSON.parse(appointmentsJson);
                window.appointmentsData = this.appointmentsData; 
            } catch (error) {
                console.error('Error parsing appointments data:', error);
                this.appointmentsData = [];
                window.appointmentsData = [];
            }
        }
    }

    setAppointmentsData(data) {
        this.appointmentsData = data;
        window.appointmentsData = data; 
    }
}

window.SchedulingManager = SchedulingManager;
