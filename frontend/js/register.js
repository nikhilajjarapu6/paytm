document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Stop page refresh

    // 1. Get data from form
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const phone = document.getElementById('phone').value;

    try {
        // 2. Send POST request to FastAPI
        // Note: Ensure your FastAPI is running on http://localhost:8000
        const response = await fetch('http://localhost:8000/users/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password,
                phone: parseInt(phone) // Ensure phone is sent as integer
            })
        });

        const data = await response.json();

        if (response.ok) {
            // 3. Registration successful, redirect to login
            alert("Registration successful! Please login.");
            window.location.href = "login.html";
        } else {
            // Handle backend errors
            alert("Error: " + (data.detail || "Registration failed"));
        }
    } catch (error) {
        console.error("Registration Error:", error);
        alert("Could not connect to the server. Is FastAPI running?");
    }
});
