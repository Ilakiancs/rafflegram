// Instagram Follower Picker - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const pickerForm = document.getElementById('pickerForm');
    const generalRadio = document.getElementById('general');
    const orientationRadio = document.getElementById('orientation');
    const countGroup = document.getElementById('countGroup');
    const timeGroup = document.getElementById('timeGroup');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const error = document.getElementById('error');
    const submitBtn = document.getElementById('submitBtn');
    const pickAgainBtn = document.getElementById('pickAgain');
    const tryAgainBtn = document.getElementById('tryAgain');

    // Toggle form fields based on picker type
    function toggleFormFields() {
        if (orientationRadio.checked) {
            countGroup.classList.add('d-none');
            timeGroup.classList.remove('d-none');
            submitBtn.innerHTML = '<i class="fas fa-clock me-2"></i>Pick from Recent Followers';
        } else {
            countGroup.classList.remove('d-none');
            timeGroup.classList.add('d-none');
            submitBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Pick Winner';
        }
    }

    // Event listeners for radio buttons
    generalRadio.addEventListener('change', toggleFormFields);
    orientationRadio.addEventListener('change', toggleFormFields);

    // Show loading state
    function showLoading() {
        hideAllStates();
        loading.classList.remove('d-none');
        loading.classList.add('slide-in');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<div class="spinner-border spinner-border-sm me-2"></div>Processing...';
    }

    // Show result state
    function showResult(data) {
        hideAllStates();
        
        const winner = data.winner;
        
        // Update winner information
        document.getElementById('winnerUsername').textContent = '@' + winner.username;
        document.getElementById('winnerFullName').textContent = winner.full_name || 'No name provided';
        document.getElementById('pickInfo').textContent = data.info;
        document.getElementById('pickTime').textContent = data.timestamp;
        
        // Handle avatar
        const avatarImg = document.getElementById('winnerAvatar');
        const avatarPlaceholder = document.getElementById('avatarPlaceholder');
        const winnerInitials = document.getElementById('winnerInitials');
        
        if (winner.profile_pic_url) {
            avatarImg.src = winner.profile_pic_url;
            avatarImg.style.display = 'block';
            avatarPlaceholder.style.display = 'none';
            
            avatarImg.onerror = function() {
                // Fallback to initials if image fails to load
                this.style.display = 'none';
                avatarPlaceholder.style.display = 'inline-flex';
                showInitials();
            };
        } else {
            avatarImg.style.display = 'none';
            avatarPlaceholder.style.display = 'inline-flex';
            showInitials();
        }
        
        function showInitials() {
            const fullName = winner.full_name || winner.username || 'U';
            const initials = fullName.split(' ')
                .map(name => name.charAt(0).toUpperCase())
                .slice(0, 2)
                .join('');
            winnerInitials.textContent = initials;
        }
        
        // Handle badges
        const privateBadge = document.getElementById('privateBadge');
        const verifiedBadge = document.getElementById('verifiedBadge');
        
        if (winner.is_private) {
            privateBadge.classList.remove('d-none');
        } else {
            privateBadge.classList.add('d-none');
        }
        
        if (winner.is_verified) {
            verifiedBadge.classList.remove('d-none');
        } else {
            verifiedBadge.classList.add('d-none');
        }
        
        result.classList.remove('d-none');
        result.classList.add('slide-in');
        resetSubmitButton();
    }

    // Show error state
    function showError(message) {
        hideAllStates();
        document.getElementById('errorMessage').textContent = message;
        error.classList.remove('d-none');
        error.classList.add('slide-in');
        resetSubmitButton();
    }

    // Hide all states
    function hideAllStates() {
        loading.classList.add('d-none');
        result.classList.add('d-none');
        error.classList.add('d-none');
        
        // Remove animation classes
        [loading, result, error].forEach(el => {
            el.classList.remove('slide-in');
        });
    }

    // Reset submit button
    function resetSubmitButton() {
        submitBtn.disabled = false;
        toggleFormFields(); // Restore original button text
    }

    // Form submission
    pickerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const pickerType = document.querySelector('input[name="pickerType"]:checked').value;
        
        if (!username) {
            showError('Please enter an Instagram username');
            return;
        }
        
        showLoading();
        
        // Prepare request data
        const requestData = {
            username: username,
            type: pickerType
        };
        
        if (pickerType === 'general') {
            requestData.count = parseInt(document.getElementById('count').value) || 50;
        } else {
            requestData.time_window = parseFloat(document.getElementById('timeWindow').value) || 1.0;
        }
        
        try {
            const response = await fetch('/api/pick', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                showResult(data);
            } else {
                showError(data.error || 'An unexpected error occurred');
            }
        } catch (err) {
            console.error('Network error:', err);
            showError('Network error. Please check your connection and try again.');
        }
    });

    // Pick again button
    pickAgainBtn.addEventListener('click', function() {
        hideAllStates();
        // Optionally clear the form or keep the same values
    });

    // Try again button
    tryAgainBtn.addEventListener('click', function() {
        hideAllStates();
    });

    // Initialize form state
    toggleFormFields();

    // Add some form validation
    document.getElementById('username').addEventListener('input', function(e) {
        // Remove @ symbol if user types it
        let value = e.target.value;
        if (value.startsWith('@')) {
            e.target.value = value.substring(1);
        }
        
        // Remove spaces
        e.target.value = e.target.value.replace(/\s/g, '');
    });

    // Add number input validation
    document.getElementById('count').addEventListener('input', function(e) {
        const value = parseInt(e.target.value);
        if (value < 10) e.target.value = 10;
        if (value > 500) e.target.value = 500;
    });

    document.getElementById('timeWindow').addEventListener('input', function(e) {
        const value = parseFloat(e.target.value);
        if (value < 0.5) e.target.value = 0.5;
        if (value > 24) e.target.value = 24;
    });

    // Health check on load (optional)
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            if (!data.api_key_configured) {
                console.warn('API key not configured');
            }
            if (!data.modules_loaded) {
                console.warn('Picker modules not loaded properly');
            }
        })
        .catch(err => {
            console.warn('Health check failed:', err);
        });
});