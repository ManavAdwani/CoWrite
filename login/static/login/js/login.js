document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent the default form submission
    // Get form data
    const email = e.target.email.value;
    const password = e.target.password.value;

    try {
        const response = await fetch('/api/login/', {  // Replace with your login API endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Successful login, you can access the tokens
            const accessToken = data.access;
            const refreshToken = data.refresh;
            const username = data.username;

            // Store tokens in localStorage or cookies (for demonstration here)
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('refreshToken', refreshToken);

            // Redirect to a new page or update UI
            window.location.href = 'textpad'; // Redirect to dashboard or home page

        } else {
            // Display error message
            document.getElementById('loginError').textContent = data.error || 'Login failed';
        }
    } catch (error) {
        console.error('Error during login:', error);
        document.getElementById('loginError').textContent = 'An error occurred during login';
    }
});
