document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Stop page refresh

    // 1. Get data from form
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        // 2. Send POST request to FastAPI
        // Note: Ensure your FastAPI is running on http://localhost:8000
        const response = await fetch('http://localhost:8000/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // 3. Store the Token and Type (Bearer)
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('token_type', data.token_type);
            
            // Optional: Store email for the profile section
            localStorage.setItem('user_email', email);

            
            // 4. Redirect to Dashboard
            window.location.href = "dashboard.html"; 
        } else {
            // Handle backend errors (e.g., 401 Unauthorized)
            alert("Error: " + (data.detail || "Invalid Credentials"));
        }
    } catch (error) {
        console.error("Login Error:", error);
        alert("Could not connect to the server. Is FastAPI running?");
    }
});