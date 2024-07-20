document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const requestForm = document.getElementById('requestForm');
    const welcomeMessage = document.getElementById('welcomeMessage');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.access) {
                localStorage.setItem('jwt_token', data.access);
                localStorage.setItem('username', username);
                alert('Login successful!');
                welcomeMessage.textContent = `Welcome, ${username}!`;
                welcomeMessage.style.display = 'block';
                requestForm.style.display = 'block';
            } else {
                alert('Login failed!');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    requestForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const serviceType = document.getElementById('serviceType').value;
        const nationality = document.getElementById('nationality').value;
        const additionalNotes = document.getElementById('additionalNotes').value;

        const token = localStorage.getItem('jwt_token');

        fetch('http://127.0.0.1:8000/api/request-housekeeper/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ service_type: serviceType, nationality, additional_notes: additionalNotes }),
        })
        .then(response => response.json())
        .then(data => {
            alert('Request submitted!');
        })
        .catch(error => console.error('Error:', error));
    });
});
