// JavaScript commun pour l'application

// Fonction pour afficher les messages flash avec animation
function showFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.classList.add('fade-in');
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000); // Disparaît après 5 secondes
    });
}

// Validation côté client pour les formulaires
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = 'red';
            isValid = false;
        } else {
            input.style.borderColor = '#ced4da';
        }
    });

    return isValid;
}

// Ajouter des event listeners aux formulaires
document.addEventListener('DOMContentLoaded', function() {
    // Afficher les messages flash
    showFlashMessages();

    // Validation des formulaires
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
                alert('Veuillez remplir tous les champs requis.');
            }
        });
    });

    // Animation pour les boutons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});

// Fonction pour afficher un spinner de chargement
function showSpinner(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    element.appendChild(spinner);
    return spinner;
}

// Fonction pour masquer le spinner
function hideSpinner(spinner) {
    if (spinner && spinner.parentNode) {
        spinner.parentNode.removeChild(spinner);
    }
}