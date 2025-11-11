document.addEventListener('DOMContentLoaded', function() {
    // Find all password toggle buttons
    const toggleButtons = document.querySelectorAll('.toggle-password');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Get the target input ID from the 'data-target' attribute
            const targetInputId = this.getAttribute('data-target');
            const targetInput = document.getElementById(targetInputId);

            if (targetInput) {
                // Toggle the input type
                if (targetInput.type === 'password') {
                    targetInput.type = 'text';
                    this.textContent = 'Hide';
                } else {
                    targetInput.type = 'password';
                    this.textContent = 'Show';
                }
            }
        });
    });
});