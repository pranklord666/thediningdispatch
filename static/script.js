document.addEventListener('DOMContentLoaded', function() {
    var dropdownButton = document.querySelector('.button-container .btn');
    var dropdownContent = document.querySelector('.dropdown_content');
    
    
    dropdownButton.addEventListener('click', function(event) {
        event.stopPropagation(); // Empêche la propagation de l'événement de clic
        dropdownContent.style.display = dropdownContent.style.display === 'flex' ? 'none' : 'flex';
    });
    
    window.addEventListener('click', function() {
        if (dropdownContent.style.display === 'flex') {
            dropdownContent.style.display = 'none';
        }
    });
    });