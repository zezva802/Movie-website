document.querySelectorAll('.genre-filter-form input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        const checkboxId = this.id;
        const label = document.querySelector(`label[for="${checkboxId}"]`);

        // Update label color based on the new checked state
        updateLabelColor(label, this.checked);
    });
});


function updateLabelColor(label, checked) {

    if (checked) {
        label.classList.add('checked');
    } else {
        label.classList.remove('checked');
    }

}


