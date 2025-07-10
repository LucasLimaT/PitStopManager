class AppointmentCalendar {
    constructor() {
        this.currentDate = new Date();
        this.selectedDate = new Date();
        this.appointments = [];
        this.viewMode = 'month';
        this.filterMode = 'month';
        
        this.initializeElements();
        this.loadAppointments();
        this.bindEvents();
        this.setupViewToggle();
        this.setupFilterToggle();
        this.updateStats();
    }

    initializeElements() {
        this.calendarContainer = document.getElementById('calendar-view');
        this.calendarGrid = document.getElementById('calendar-grid');
        this.calendarTitle = document.getElementById('calendar-title');
        this.prevBtn = document.getElementById('prev-month');
        this.nextBtn = document.getElementById('next-month');
        this.todayBtn = document.getElementById('today-btn');
        this.viewModeToggle = document.getElementById('view-mode-toggle');
        this.filterOptions = document.querySelectorAll('.filter-option');
        this.currentFilterSpan = document.getElementById('current-filter');
        this.tooltip = document.getElementById('event-tooltip');
    }

    bindEvents() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.goToPreviousPeriod());
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.goToNextPeriod());
        }
        if (this.todayBtn) {
            this.todayBtn.addEventListener('click', () => this.goToToday());
        }

        document.addEventListener('click', (e) => {
            const sidebar = document.querySelector('.appointment-sidebar');
            if (sidebar && sidebar.style.display === 'block') {
                if (!sidebar.contains(e.target) && !e.target.closest('.calendar-day')) {
                    sidebar.style.display = 'none';
                }
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const sidebar = document.querySelector('.appointment-sidebar');
                if (sidebar && sidebar.style.display === 'block') {
                    sidebar.style.display = 'none';
                }
            }
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.calendar-event')) {
                this.hideTooltip();
            }
        });
    }

    setupViewToggle() {
        const calendarView = document.getElementById('calendar-view');
        const listView = document.getElementById('list-view');
        
        if (this.viewModeToggle) {
            this.viewModeToggle.addEventListener('change', (e) => {
                if (e.target.checked) {
                    if (calendarView) calendarView.style.display = 'none';
                    if (listView) listView.style.display = 'block';
                    this.viewMode = 'list';
                } else {
                    if (calendarView) calendarView.style.display = 'block';
                    if (listView) listView.style.display = 'none';
                    this.viewMode = 'calendar';
                }
            });
        }
    }

    setupFilterToggle() {
        const dropdownToggle = document.getElementById('view-filter-dropdown');
        const dropdownMenu = document.getElementById('filter-dropdown-menu');
        
        if (dropdownToggle && dropdownMenu) {
            dropdownToggle.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropdownMenu.classList.toggle('show');
                dropdownToggle.classList.toggle('show');
            });
            
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.filter-dropdown')) {
                    dropdownMenu.classList.remove('show');
                    dropdownToggle.classList.remove('show');
                }
            });
        }
        
        this.filterOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.preventDefault();
                const filter = e.target.dataset.filter;
                
                this.filterOptions.forEach(opt => opt.classList.remove('active'));
                e.target.classList.add('active');
                
                if (this.currentFilterSpan) {
                    this.currentFilterSpan.textContent = e.target.textContent;
                }
                
                this.setFilterMode(filter);
                
                if (dropdownMenu) {
                    dropdownMenu.classList.remove('show');
                    dropdownToggle.classList.remove('show');
                }
            });
        });
    }

    setFilterMode(mode) {
        this.filterMode = mode;
        this.renderCalendar();
    }

    loadAppointments() {
        const appointmentsDataElement = document.getElementById('appointments-data');
        if (appointmentsDataElement) {
            try {
                const appointmentsJson = appointmentsDataElement.dataset.appointmentsJson;
                this.appointments = JSON.parse(appointmentsJson);
                window.appointmentsData = this.appointments;
            } catch (error) {
                console.error('Error parsing appointments data:', error);
                this.appointments = [];
                window.appointmentsData = [];
            }
        } else if (window.appointmentsData) {
            this.appointments = window.appointmentsData;
        } else {
            this.appointments = [];
        }
        console.log('Loaded appointments:', this.appointments);
        this.renderCalendar();
    }

    goToPreviousPeriod() {
        if (this.filterMode === 'month') {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
        } else if (this.filterMode === 'week') {
            this.currentDate.setDate(this.currentDate.getDate() - 7);
        } else if (this.filterMode === 'day') {
            this.currentDate.setDate(this.currentDate.getDate() - 1);
        }
        this.renderCalendar();
    }

    goToNextPeriod() {
        if (this.filterMode === 'month') {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
        } else if (this.filterMode === 'week') {
            this.currentDate.setDate(this.currentDate.getDate() + 7);
        } else if (this.filterMode === 'day') {
            this.currentDate.setDate(this.currentDate.getDate() + 1);
        }
        this.renderCalendar();
    }

    goToToday() {
        this.currentDate = new Date();
        this.selectedDate = new Date();
        this.renderCalendar();
    }

    renderCalendar() {
        this.updateTitle();
        if (this.filterMode === 'month') {
            this.renderMonthGrid();
        } else if (this.filterMode === 'week') {
            this.renderWeekGrid();
        } else if (this.filterMode === 'day') {
            this.renderDayGrid();
        }
    }

    updateTitle() {
        const monthNames = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ];
        
        const month = monthNames[this.currentDate.getMonth()];
        const year = this.currentDate.getFullYear();
        
        if (this.calendarTitle) {
            if (this.filterMode === 'month') {
                this.calendarTitle.textContent = `${month} ${year}`;
            } else if (this.filterMode === 'week') {
                this.calendarTitle.textContent = `Semana - ${month} ${year}`;
            } else if (this.filterMode === 'day') {
                const day = this.currentDate.getDate();
                this.calendarTitle.textContent = `${day} de ${month} ${year}`;
            }
        }
    }

    renderMonthGrid() {
        if (!this.calendarGrid) return;

        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();

        this.calendarGrid.innerHTML = '';

        const dayHeaders = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
        dayHeaders.forEach(day => {
            const header = document.createElement('div');
            header.className = 'calendar-day-header';
            header.textContent = day;
            this.calendarGrid.appendChild(header);
        });

        for (let i = 0; i < startingDayOfWeek; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day other-month';
            this.calendarGrid.appendChild(emptyDay);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = this.createDayElement(year, month, day);
            this.calendarGrid.appendChild(dayElement);
        }

        const totalCells = this.calendarGrid.children.length - 7; 
        const remainingCells = 42 - totalCells; 
        for (let i = 0; i < remainingCells; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day other-month';
            this.calendarGrid.appendChild(emptyDay);
        }
    }

    renderWeekGrid() {
        if (!this.calendarGrid) return;

        const startOfWeek = new Date(this.currentDate);
        startOfWeek.setDate(this.currentDate.getDate() - this.currentDate.getDay());

        this.calendarGrid.innerHTML = '';

        const dayHeaders = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
        dayHeaders.forEach(day => {
            const header = document.createElement('div');
            header.className = 'calendar-day-header';
            header.textContent = day;
            this.calendarGrid.appendChild(header);
        });

        for (let i = 0; i < 7; i++) {
            const date = new Date(startOfWeek);
            date.setDate(startOfWeek.getDate() + i);
            const dayElement = this.createDayElement(date.getFullYear(), date.getMonth(), date.getDate());
            this.calendarGrid.appendChild(dayElement);
        }
    }

    renderDayGrid() {
        if (!this.calendarGrid) return;

        this.calendarGrid.innerHTML = '';

        const dayElement = this.createDayElement(
            this.currentDate.getFullYear(),
            this.currentDate.getMonth(),
            this.currentDate.getDate(),
            true 
        );
        dayElement.style.minHeight = '400px';
        dayElement.style.gridColumn = '1 / -1';
        this.calendarGrid.appendChild(dayElement);
    }

    createDayElement(year, month, day, isFullDay = false) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        
        const date = new Date(year, month, day);
        const today = new Date();
        
        if (this.isSameDay(date, today)) {
            dayElement.classList.add('today');
        }
        
        if (this.isSameDay(date, this.selectedDate)) {
            dayElement.classList.add('selected');
        }

        const dayNumber = document.createElement('div');
        dayNumber.className = 'calendar-day-number';
        dayNumber.textContent = day;
        dayElement.appendChild(dayNumber);

        const eventsContainer = document.createElement('div');
        eventsContainer.className = 'calendar-events';
        
        const dayAppointments = this.getAppointmentsForDay(date);
        
        dayAppointments.forEach(appointment => {
            const eventElement = this.createEventElement(appointment, isFullDay);
            eventsContainer.appendChild(eventElement);
        });

        dayElement.appendChild(eventsContainer);

        dayElement.addEventListener('click', () => {
            this.selectDay(date);
        });

        return dayElement;
    }

    createEventElement(appointment, isFullDay = false) {
        const eventElement = document.createElement('div');
        eventElement.className = 'calendar-event';
        
        const eventTime = new Date(appointment.data_do_agendamento);
        const now = new Date();
        
        if (eventTime < now) {
            eventElement.classList.add('event-success'); 
        } else if (this.isWithinHours(eventTime, 24)) {
            eventElement.classList.add('event-warning'); 
        } else {
            
        }

        const timeStr = eventTime.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        const vehicleInfo = appointment.vehicle_info || 'Veículo N/D';
        
        if (isFullDay) {
            eventElement.innerHTML = `
                <strong>${timeStr}</strong><br>
                ${vehicleInfo}<br>
                <small>Responsável: ${appointment.responsavel}</small>
            `;
            eventElement.style.padding = '8px';
            eventElement.style.marginBottom = '4px';
        } else {
            eventElement.textContent = `${timeStr} - ${vehicleInfo}`;
        }
        
        eventElement.addEventListener('mouseenter', (e) => {
            this.showTooltip(e, appointment);
        });
        
        eventElement.addEventListener('mouseleave', () => {
            this.hideTooltip();
        });

        eventElement.addEventListener('click', (e) => {
            e.stopPropagation();
            this.showAppointmentDetails(appointment);
        });

        return eventElement;
    }

    getAppointmentsForDay(date) {
        return this.appointments.filter(appointment => {
            const appointmentDate = new Date(appointment.data_do_agendamento);
            return this.isSameDay(appointmentDate, date);
        });
    }

    isSameDay(date1, date2) {
        return date1.getFullYear() === date2.getFullYear() &&
               date1.getMonth() === date2.getMonth() &&
               date1.getDate() === date2.getDate();
    }

    isWithinHours(date, hours) {
        const now = new Date();
        const diffMs = date.getTime() - now.getTime();
        const diffHours = diffMs / (1000 * 60 * 60);
        return diffHours > 0 && diffHours <= hours;
    }

    selectDay(date) {
        this.selectedDate = new Date(date);
        
        document.querySelectorAll('.calendar-day').forEach(day => {
            day.classList.remove('selected');
        });
        
        const dayElements = document.querySelectorAll('.calendar-day');
        dayElements.forEach(dayElement => {
            const dayNumber = dayElement.querySelector('.calendar-day-number');
            if (dayNumber && parseInt(dayNumber.textContent) === date.getDate()) {
                if (!dayElement.classList.contains('other-month')) {
                    dayElement.classList.add('selected');
                }
            }
        });
        
        this.showDayAppointments(date);
    }

    showDayAppointments(date) {
        const appointments = this.getAppointmentsForDay(date);
        let sidebar = document.querySelector('.appointment-sidebar');
        
        if (!sidebar) {
            sidebar = document.createElement('div');
            sidebar.className = 'appointment-sidebar';
            document.body.appendChild(sidebar);
        }
        
        const dateStr = date.toLocaleDateString('pt-BR');
        sidebar.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0;">Agendamentos - ${dateStr}</h3>
                <button onclick="this.parentElement.parentElement.style.display='none'" class="btn btn-sm btn-outline-secondary">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            ${appointments.length > 0 ? 
                appointments.map(apt => `
                    <div class="appointment-item">
                        <div class="appointment-time">${new Date(apt.data_do_agendamento).toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'})}</div>
                        <div class="appointment-vehicle">${apt.vehicle_info}</div>
                        <div class="appointment-responsible">Responsável: ${apt.responsavel}</div>
                        <div class="appointment-actions">
                            <a href="/scheduling/${apt.id}/" class="btn btn-sm btn-outline-primary">Ver</a>
                            <a href="/scheduling/${apt.id}/edit/" class="btn btn-sm btn-outline-secondary">Editar</a>
                        </div>
                    </div>
                `).join('') 
                : '<p class="text-muted">Nenhum agendamento para este dia.</p>'
            }
            <div class="mt-3">
                <a href="/scheduling/create/?date=${date.toISOString().split('T')[0]}" class="btn btn-primary btn-sm w-100">
                    <i class="fas fa-plus"></i> Novo Agendamento
                </a>
            </div>
        `;
        
        sidebar.style.display = 'block';
        sidebar.classList.add('show');
    }

    showTooltip(event, appointment) {
        if (!this.tooltip) return;

        const eventTime = new Date(appointment.data_do_agendamento);
        const timeStr = eventTime.toLocaleString('pt-BR');
        
        this.tooltip.innerHTML = `
            <strong>${appointment.vehicle_info}</strong><br>
            <strong>Horário:</strong> ${timeStr}<br>
            <strong>Responsável:</strong> ${appointment.responsavel}<br>
            ${appointment.service_order_id ? `<strong>OS:</strong> #${appointment.service_order_id}` : ''}
        `;

        const rect = event.target.getBoundingClientRect();
        this.tooltip.style.left = rect.left + (rect.width / 2) + 'px';
        this.tooltip.style.top = rect.top - 10 + 'px';
        this.tooltip.classList.add('show');
    }

    hideTooltip() {
        if (this.tooltip) {
            this.tooltip.classList.remove('show');
        }
    }

    showAppointmentDetails(appointment) {
        
        window.location.href = `/scheduling/${appointment.id}/`;
    }

    updateStats() {
        const now = new Date();
        const appointments = this.appointments || [];
        
        const todayCount = appointments.filter(apt => {
            const aptDate = new Date(apt.data_do_agendamento);
            return aptDate.toDateString() === now.toDateString();
        }).length;
        
        const weekStart = new Date(now);
        weekStart.setDate(now.getDate() - now.getDay());
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekStart.getDate() + 6);
        
        const weekCount = appointments.filter(apt => {
            const aptDate = new Date(apt.data_do_agendamento);
            return aptDate >= weekStart && aptDate <= weekEnd;
        }).length;
        
        const monthCount = appointments.filter(apt => {
            const aptDate = new Date(apt.data_do_agendamento);
            return aptDate.getMonth() === now.getMonth() && 
                   aptDate.getFullYear() === now.getFullYear();
        }).length;
        
        const todayElement = document.getElementById('today-count');
        const weekElement = document.getElementById('week-count');
        const monthElement = document.getElementById('month-count');
        
        if (todayElement) todayElement.textContent = todayCount;
        if (weekElement) weekElement.textContent = weekCount;
        if (monthElement) monthElement.textContent = monthCount;
    }
}


window.setAppointmentsData = function(data) {
    window.appointmentsData = data;
    if (window.appointmentCalendar) {
        window.appointmentCalendar.loadAppointments();
        window.appointmentCalendar.updateStats();
    }
};


document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        if (document.getElementById('calendar-view')) {
            window.appointmentCalendar = new AppointmentCalendar();
        }
    }, 200);

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('vehicle_id')) {
        const viewToggle = document.getElementById('view-mode-toggle');
        const calendarView = document.getElementById('calendar-view');
        const listView = document.getElementById('list-view');
        if (viewToggle) {
            viewToggle.checked = true;
            if (calendarView) calendarView.style.display = 'none';
            if (listView) listView.style.display = 'block';
        }
    }
});
