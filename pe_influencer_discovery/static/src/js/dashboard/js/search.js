document.addEventListener('DOMContentLoaded', function() {
    // Get all dropdown buttons
    const dropdownButtons = document.querySelectorAll('.dropbtn');

    // Function to close all dropdowns
    const closeAllDropdowns = () => {
        const dropdowns = document.querySelectorAll('.dropdown-content');
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    };

    // Add click event to each dropdown button
    dropdownButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.stopPropagation();

            // Close all other dropdowns first
            const allDropdowns = document.querySelectorAll('.dropdown-content');
            allDropdowns.forEach(dropdown => {
                if (dropdown !== this.nextElementSibling) {
                    dropdown.classList.remove('show');
                }
            });

            // Toggle the clicked dropdown
            const dropdownContent = this.nextElementSibling;
            dropdownContent.classList.toggle('show');
        });
    });

    // Close dropdowns when clicking outside
    window.addEventListener('click', function() {
        closeAllDropdowns();
    });

    // Close dropdowns when pressing ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeAllDropdowns();
        }
    });
});