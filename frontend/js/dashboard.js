const sendBtn = document.querySelector('.send');
const modal = document.getElementById('sendModal');
const closeBtn = document.getElementById('closeModal');
const token = localStorage.getItem('access_token');

// Open Modal
sendBtn.addEventListener('click', () => {
    modal.classList.add('active');
});

// Close Modal when clicking (X)
closeBtn.addEventListener('click', () => {
    modal.classList.remove('active');
});

// Close Modal when clicking outside the box
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('active');
    }
});

const receiveBtn = document.querySelector('.receive');
const receiveModal = document.getElementById('receiveModal');
const closeReceive = document.getElementById('closeReceive');
const qrImage = document.getElementById('qrImage');

// Open Receive Modal
receiveBtn.addEventListener('click', () => {
    // Generate a random ID so the QR code looks different each time
    const randomId = Math.floor(Math.random() * 1000);
    // Using a QR placeholder API
    qrImage.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=PaytmUser${randomId}`;
    
    receiveModal.classList.add('active');
});

// Close Receive Modal
closeReceive.addEventListener('click', () => {
    receiveModal.classList.remove('active');
});

// Close when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === receiveModal) {
        receiveModal.classList.remove('active');
    }
});

function toggleDetails(element) {
    // Finds the parent container of the clicked item
    const container = element.closest('.tx-container');
    
    // Toggle the 'active' class to show/hide details
    container.classList.toggle('active');

    // Optional: Close other open details when one is opened
    document.querySelectorAll('.tx-container').forEach(item => {
        if (item !== container) {
            item.classList.remove('active');
        }
    });
}

// Select Elements
const editModal = document.getElementById('editProfileModal');
const editBtn = document.querySelector('.edit-badge');
const closeEditBtn = document.getElementById('closeEdit');
const editForm = document.getElementById('editProfileForm');

// Elements on the Dashboard to be updated
const displayName = document.querySelector('.user-info h3');
const displayUpi = document.querySelector('.upi-id');
const displayEmail = document.querySelector('.email');

// 1. Open Modal
editBtn.addEventListener('click', () => {
    editModal.classList.add('active');
});

// 2. Close Modal
closeEditBtn.addEventListener('click', () => {
    editModal.classList.remove('active');
});

// 3. Update Function
editForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        name: document.getElementById('editName').value,
        upi_id: document.getElementById('editUpi').value,
        email: document.getElementById('editEmail').value,
        password: document.getElementById('editPassword').value
    };

    try {
        const res = await fetch("http://localhost:8000/users/update", {
            method: "PUT",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(err.detail || "Profile update failed");
            return;
        }

        const updatedUser = await res.json();

        
        displayName.innerText = updatedUser.name;
        displayUpi.innerText = updatedUser.upi_id;
        displayEmail.innerText = updatedUser.email;

        alert("Profile Updated Successfully!");
        editModal.classList.remove('active');

    } catch (error) {
        console.error("Update Error:", error);
        alert("Server error. Try again later.");
    }
});


// Close if clicked outside
window.addEventListener('click', (e) => {
    if (e.target === editModal) {
        editModal.classList.remove('active');
    }
});

const historyModal = document.getElementById('historyModal');
const seeAllBtn = document.querySelector('.see-all-btn');
const closeHistory = document.getElementById('closeHistory');

// Open History
seeAllBtn.addEventListener('click', () => {
    historyModal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevents background scroll
});

// Close History
closeHistory.addEventListener('click', () => {
    historyModal.classList.remove('active');
    document.body.style.overflow = 'auto'; // Re-enables background scroll
});

// Your existing toggleDetails(element) function will 
// automatically work here because we used the same classes!

function triggerSearch() {
    const query = document.getElementById('dashboardSearchInput').value.trim();
    const historyModal = document.getElementById('historyModal');
    const historyTitle = historyModal.querySelector('h3');

    if (query === "") {
        alert("Please enter a name or amount to search.");
        return;
    }

    // Update the Modal Header to show what was searched
    historyTitle.innerText = `Results for: "${query}"`;

    // Open the Modal
    historyModal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Optional: You could actually filter the list here 
    // For now, it opens the "See All" view as requested
}

// Allow pressing "Enter" key to search as well
document.getElementById('dashboardSearchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        triggerSearch();
    }
});

function handleLogout() {
    // Optional: Add a confirmation pop-up
    const confirmLogout = confirm("Are you sure you want to log out?");
    
    if (confirmLogout) {
        // Add a small fade-out effect for fun
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.5s ease';
        
        // Redirect to login page after 500ms
        setTimeout(() => {
            window.location.href = "login.html"; // Make sure the filename matches yours
        }, 500);
    }
}

// Function to fetch and render transactions
async function loadTransactions() {
    const token = localStorage.getItem('access_token');
    const txListContainer = document.querySelector('.tx-list');

    // 1. Check if token exists, otherwise redirect to login
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    try {
        // 2. Fetch from FastAPI
        const response = await fetch('http://localhost:8000/transactions/mytransactions', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const transactions = await response.json();
            
            // 3. Clear existing static items (except the "See All" button)
            txListContainer.innerHTML = '';

            // 4. Loop through data and create HTML
            transactions.forEach(tx => {
                const isCredit = tx.amount > 0;
                const txHTML = `
                    <div class="tx-container">
                        <div class="tx ${isCredit ? 'credit' : 'debit'}" onclick="toggleDetails(this)">
                            <div class="tx-info">
                                <span class="name">${tx.receiver_id}</span>
                                <span class="date">${new Date(tx.created_at).toLocaleString()} • ${tx.payment_method}</span>
                            </div>
                            <div class="tx-right">
                                <span class="amount">${isCredit ? '+' : '-'} ₹${Math.abs(tx.amount)}</span>
                                <span class="arrow-icon">▼</span>
                            </div>
                        </div>
                        <div class="tx-details">
                            <div class="details-grid">
                                <div class="detail-item"><strong>Txn ID</strong><span>${tx.txn_id}</span></div>
                                <div class="detail-item"><strong>Status</strong><span class="status-success">Success</span></div>
                                <div class="detail-item"><strong>Category</strong><span>${tx.payment_method}</span></div>
                                <div class="detail-item"><strong>Note</strong><span>${tx.description || 'N/A'}</span></div>
                            </div>
                        </div>
                    </div>`;
                txListContainer.insertAdjacentHTML('beforeend', txHTML);
            });
        } else {
            console.error("Failed to fetch transactions");
        }
    } catch (error) {
        console.error("Server Error:", error);
    }
}



//function for handling sending money
const sendMoney=document.getElementById('sendMoneyForm')
sendMoney.addEventListener('submit',async(e)=>{
    e.preventDefault()

    const payload={
        receiver_id: document.getElementById('sendReceiver').value,
        amount: parseFloat(document.getElementById('sendAmount').value),
        payment_method: document.getElementById('sendMethod').value,
        description: document.getElementById('sendDescription').value
    }

    try {
        const res=await fetch("http://localhost:8000/transactions/send",{
            method:"POST",
            headers:{
                'Authorization':`Bearer ${token}`,
                'Content-type':'application/json'
            },
            body:JSON.stringify(payload)
        })

        if (res){
            const result=await res.json()
            alert("Payment Successful! Txn ID: " + result.txn_id);

            sendMoney.reset(); 
            document.getElementById('sendModal').classList.remove('active'); 
            
            loadTransactions(); 
        }
        else{
            const errorData=await res.json()
            alert("Payment Failed: " + (errorData.detail || "Unknown Error"));
        }
    } catch (error) {
        console.error("Connection Error:", error);
        alert("Server is down. Please try again later.");
    }
})


// Call the function when the page loads
document.addEventListener('DOMContentLoaded', loadTransactions);