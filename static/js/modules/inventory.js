document.addEventListener('DOMContentLoaded', function() {
    const toggleInput = document.getElementById('view-mode-toggle');
    const cardView = document.getElementById('card-view');
    const listView = document.getElementById('list-view');

    if (toggleInput && cardView && listView) {
        toggleInput.addEventListener('change', function() {
            if (this.checked) {
                cardView.classList.add('hidden');
                listView.classList.add('show');
            } else {
                cardView.classList.remove('hidden');
                listView.classList.remove('show');
            }
        });
        if (toggleInput.checked) {
            cardView.classList.add('hidden');
            listView.classList.add('show');
        } else {
            cardView.classList.remove('hidden');
            listView.classList.remove('show');
        }
    }
});
