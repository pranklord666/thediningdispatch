document.addEventListener('DOMContentLoaded', function() {
    var dropdownButtons = document.querySelectorAll('.button-container .btn');
    var dropdownContents = document.querySelectorAll('.dropdown_content');

    dropdownButtons.forEach(function(button, index) {
        button.addEventListener('click', function(event) {
            event.stopPropagation(); // Prevent the click event from propagating
            var dropdownContent = dropdownContents[index];
            dropdownContent.style.display = dropdownContent.style.display === 'flex' ? 'none' : 'flex';
        });
    });

    window.addEventListener('click', function() {
        dropdownContents.forEach(function(dropdownContent) {
            if (dropdownContent.style.display === 'flex') {
                dropdownContent.style.display = 'none';
            }
        });
    });
});
