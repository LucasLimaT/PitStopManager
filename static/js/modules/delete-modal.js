
document.addEventListener('DOMContentLoaded', function() {
    const deleteModal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const itemInfo = document.getElementById('itemInfo');
    
    if (deleteModal && deleteForm && confirmDeleteBtn && itemInfo) {
        
        deleteModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const itemId = button.getAttribute('data-item-id');
            const itemName = button.getAttribute('data-item-name');
            const itemType = button.getAttribute('data-item-type');
            
            itemInfo.textContent = `${itemType}: ${itemName}`;
            
            let deleteUrl = '';
            const currentPath = window.location.pathname;
            
            if (currentPath.includes('/services/')) {
                deleteUrl = `/services/${itemId}/delete/`;
            } else if (currentPath.includes('/customers/')) {
                deleteUrl = `/customers/${itemId}/delete/`;
            } else if (currentPath.includes('/vehicles/')) {
                deleteUrl = `/vehicles/${itemId}/delete/`;
            } else if (currentPath.includes('/scheduling/')) {
                deleteUrl = `/scheduling/${itemId}/delete/`;
            } else if (currentPath.includes('/inventory/')) {
                deleteUrl = `/inventory/${itemId}/delete/`;
            }
            
            deleteForm.action = deleteUrl;
            
            confirmDeleteBtn.innerHTML = '<i class="fas fa-trash-alt me-1"></i>Sim, Excluir';
            confirmDeleteBtn.disabled = false;
        });
        
        deleteForm.addEventListener('submit', function() {
            confirmDeleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Excluindo...';
            confirmDeleteBtn.disabled = true;
        });
    }
});
