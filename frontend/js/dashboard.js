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

// Global variable to store current user data
let currentUser = null;

// Load logged-in user's profile and populate dashboard
async function loadProfile() {
    const token = localStorage.getItem('access_token');
    const email = localStorage.getItem('user_email');
    console.log(email);

    if (!token) return; // will redirect elsewhere if needed

    // If we don't have the email stored, skip (could request a /me endpoint instead)
    let useEmail = email;
    if (!useEmail) {
        // Try to decode JWT payload to get the email (sub) without verification
        try {
            const parts = token.split('.');
            if (parts.length === 3) {
                const payload = JSON.parse(decodeURIComponent(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')).split('').map(function(c) {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }).join('')));
                useEmail = payload.sub || useEmail;
            }
        } catch (e) {
            console.warn('Could not decode token for email fallback', e);
        }
    }
    if (!useEmail) return;

    try {
        const res = await fetch('http://localhost:8000/users/find_by_email', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: useEmail })
        });



        if (!res.ok) {
            console.warn('Could not load profile:', res.status);
            try { const dbg = await res.json(); console.warn(dbg); } catch (e) {}
            return;
        }

        const user = await res.json();
        if (user) {
            currentUser = user; // Store user data globally
            if (displayName) displayName.innerText = user.name ;
            if (displayUpi) displayUpi.innerText = user.upi_id || displayUpi.innerText;
            if (displayEmail) displayEmail.innerText = user.email || displayEmail.innerText;
            // persist email for future loads
            if (!email && user.email) localStorage.setItem('user_email', user.email);
            // Update member since (year) and last-updated fields
            try {
                const memberTag = document.querySelector('.user-tags .tag:not(.kyc)');
                if (memberTag && user.created_at) {
                    const year = new Date(user.created_at).getFullYear();
                    memberTag.innerText = `Member since ${year}`;
                }

                const lastEl = document.querySelector('.last-updated');
                const lastDate = user.updated_at || user.created_at;
                if (lastEl && lastDate) {
                    lastEl.innerText = `Last updated: ${new Date(lastDate).toLocaleString()}`;
                }
            } catch (e) {
                console.warn('Could not set member/last-updated:', e);
            }
        }

    } catch (err) {
        console.error('Profile load error:', err);
    }
}

// 1. Open Modal
editBtn.addEventListener('click', () => {
    // Populate form fields with current user data
    if (currentUser) {
        document.getElementById('editName').value = currentUser.name || '';
        document.getElementById('editUpi').value = currentUser.upi_id || '';
        document.getElementById('editEmail').value = currentUser.email || '';
        document.getElementById('editPhone').value = currentUser.phone || '';
        // Note: Password field is intentionally left empty for security reasons
    }
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
        password: document.getElementById('editPassword').value,
        phone: document.getElementById('editPhone').value
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
        // displayMobile.innerText = updatedUser.mobile;

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

// Close History when clicking outside the modal content
window.addEventListener('click', (e) => {
    if (e.target === historyModal) {
        historyModal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
});

// Your existing toggleDetails(element) function will 
// Global variable to store transactions for filtering/sorting
let allTransactions = [];

// Function to render transactions in the history modal
function renderTransactions(transactions, containerId = '.tx-list') {
    const container = document.querySelector(containerId);
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!transactions || transactions.length === 0) {
        container.innerHTML = `
            <div class="no-transactions" style="padding:20px;text-align:center;color:#fff;opacity:0.9">
                <p style="margin:0;font-weight:600">No transactions found</p>
                <p style="margin:6px 0 0;font-size:13px;color:rgba(255,255,255,0.8)">Try adjusting your filters.</p>
            </div>`;
        return;
    }
    
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
                        <div class="detail-item"><strong>Receiver ID</strong><span>${tx.receiver_id}</span></div>
                        <div class="detail-item"><strong>Status</strong><span class="status-success">Success</span></div>
                        <div class="detail-item"><strong>Payment Type</strong><span>${tx.payment_method}</span></div>
                        <div class="detail-item"><strong>Note</strong><span>${tx.description || 'N/A'}</span></div>
                    </div>
                </div>
            </div>`;
        container.insertAdjacentHTML('beforeend', txHTML);
    });
}

// Sort by Date (newest first, then oldest first)
function sortByDate() {
    const dateBtn = document.querySelector('[data-sort="date"]');
    const isAscending = dateBtn.classList.toggle('ascending');
    
    const sorted = [...allTransactions].sort((a, b) => {
        const dateA = new Date(a.created_at);
        const dateB = new Date(b.created_at);
        return isAscending ? dateA - dateB : dateB - dateA;
    });
    
    // Update all filter buttons to show which is active
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active', 'ascending', 'descending');
    });
    dateBtn.classList.add('active');
    dateBtn.classList.add(isAscending ? 'ascending' : 'descending');
    
    renderTransactions(sorted, '.transactions .tx-list');
}

// Sort by Amount (highest to lowest, then lowest to highest)
function sortByAmount() {
    const amountBtn = document.querySelector('[data-sort="amount"]');
    const isAscending = amountBtn.classList.toggle('ascending');
    
    const sorted = [...allTransactions].sort((a, b) => {
        const amountA = Math.abs(a.amount);
        const amountB = Math.abs(b.amount);
        return isAscending ? amountA - amountB : amountB - amountA;
    });
    
    // Update all filter buttons to show which is active
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active', 'ascending', 'descending');
    });
    amountBtn.classList.add('active');
    amountBtn.classList.add(isAscending ? 'ascending' : 'descending');
    
    renderTransactions(sorted, '.transactions .tx-list');
}

// Sort by Payment Method
function sortByPaymentMode() {
    const modeBtn = document.querySelector('[data-sort="mode"]');
    const isAscending = modeBtn.classList.toggle('ascending');
    
    const sorted = [...allTransactions].sort((a, b) => {
        const modeA = a.payment_method.toLowerCase();
        const modeB = b.payment_method.toLowerCase();
        return isAscending ? modeA.localeCompare(modeB) : modeB.localeCompare(modeA);
    });
    
    // Update all filter buttons to show which is active
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active', 'ascending', 'descending');
    });
    modeBtn.classList.add('active');
    modeBtn.classList.add(isAscending ? 'ascending' : 'descending');
    
    renderTransactions(sorted, '.transactions .tx-list');
}

// Reset filters to show all transactions
function resetFilters() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active', 'ascending', 'descending');
    });
    renderTransactions(allTransactions, '.transactions .tx-list');
}

function triggerSearch() {
    const query = document.getElementById('dashboardSearchInput').value.trim().toLowerCase();
    const historyTitle = historyModal.querySelector('h3');
    const historyListContainer = historyModal.querySelector('.tx-list');

    if (query === "") {
        alert("Please enter a name or amount to search.");
        return;
    }

    // Get all transactions from the page or fetch them
    // For now, we'll fetch fresh transactions and filter
    
    if (!token) {
        alert("Not authenticated");
        return;
    }

    // Fetch transactions and filter by query
    fetch('http://localhost:8000/transactions/mytransactions', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(res => {
        if (!res.ok) throw new Error('Failed to fetch transactions');
        return res.json();
    })
    .then(transactions => {
        // Filter transactions by multiple fields: receiver_id, txn_id, payment_method, description, date, amount
        const filtered = transactions.filter(tx => {
            const receiver = (tx.receiver_id || '').toString().toLowerCase();
            const txnId = (tx.txn_id || '').toString().toLowerCase();
            const method = (tx.payment_method || '').toString().toLowerCase();
            const description = (tx.description || '').toString().toLowerCase();
            const dateStr = new Date(tx.created_at).toLocaleString().toLowerCase();
            const amount = Math.abs(tx.amount).toString();
            
            // Match query against any field
            return receiver.includes(query) || 
                   txnId.includes(query) || 
                   method.includes(query) || 
                   description.includes(query) || 
                   dateStr.includes(query) || 
                   amount.includes(query);
        });

        // Update the Modal Header to show what was searched
        historyTitle.innerText = `Results for: "${query}"`;

        // Clear the list container
        historyListContainer.innerHTML = '';

        // If no results, show message
        if (filtered.length === 0) {
            historyListContainer.innerHTML = `
                <div style="padding:20px;text-align:center;color:#fff;opacity:0.9">
                    <p style="margin:0;font-weight:600">No results found</p>
                    <p style="margin:6px 0 0;font-size:13px;color:rgba(255,255,255,0.8)">Try searching with a different name or amount.</p>
                </div>`;
        } else {
            // Render filtered transactions
            filtered.forEach(tx => {
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
                                <div class="detail-item"><strong>Receiver ID</strong><span>${tx.receiver_id}</span></div>
                                <div class="detail-item"><strong>Status</strong><span class="status-success">Success</span></div>
                                <div class="detail-item"><strong>Payment Type</strong><span>${tx.payment_method}</span></div>
                                <div class="detail-item"><strong>Note</strong><span>${tx.description || 'N/A'}</span></div>
                            </div>
                        </div>
                    </div>`;
                historyListContainer.insertAdjacentHTML('beforeend', txHTML);
            });
        }

        // Open the Modal
        historyModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    })
    .catch(error => {
        console.error('Search error:', error);
        alert('Failed to search transactions');
    });
}


document.getElementById('dashboardSearchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        triggerSearch();
    }
});

function handleLogout() {

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
    const txListContainer = document.querySelector('.transactions .tx-list');
    const historyListContainer = historyModal ? historyModal.querySelector('.tx-list') : null;

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
            
            // Store all transactions for filtering/sorting
            allTransactions = transactions;

            // 3. Clear existing dashboard and history lists
            txListContainer.innerHTML = '';
            if (historyListContainer) historyListContainer.innerHTML = '';

            // If no transactions, show a friendly empty state and hide "See All"
            if (!transactions || transactions.length === 0) {
                txListContainer.innerHTML = `
                    <div class="no-transactions" style="padding:20px;text-align:center;color:#fff;opacity:0.9">
                        <p style="margin:0;font-weight:600">No transactions yet</p>
                        <p style="margin:6px 0 0;font-size:13px;color:rgba(255,255,255,0.8)">Your recent activity will appear here.</p>
                    </div>`;
                if (historyListContainer) historyListContainer.innerHTML = `<div style="padding:20px;text-align:center;">No transactions found.</div>`;
                if (seeAllBtn) seeAllBtn.style.display = 'none';
                return;
            } else {
                if (seeAllBtn) seeAllBtn.style.display = '';
            }

            // 4. Render only the most recent 3 transactions on the dashboard
            const recent = transactions.slice(0, 3);
            recent.forEach(tx => {
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
                                <div class="detail-item"><strong>Receiver ID</strong><span>${tx.receiver_id}</span></div>
                                <div class="detail-item"><strong>Status</strong><span class="status-success">Success</span></div>
                                <div class="detail-item"><strong>Payment Type</strong><span>${tx.payment_method}</span></div>
                                <div class="detail-item"><strong>Note</strong><span>${tx.description || 'N/A'}</span></div>
                            </div>
                        </div>
                    </div>`;
                txListContainer.insertAdjacentHTML('beforeend', txHTML);
            });

            // 5. Populate the history modal with the full transaction list (see-all view)
            if (historyListContainer) {
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
                                    <div class="detail-item"><strong>Receiver ID</strong><span>${tx.receiver_id}</span></div>
                                    <div class="detail-item"><strong>Status</strong><span class="status-success">Success</span></div>
                                    <div class="detail-item"><strong>Payment Type</strong><span>${tx.payment_method}</span></div>
                                    <div class="detail-item"><strong>Note</strong><span>${tx.description || 'N/A'}</span></div>
                                </div>
                            </div>
                        </div>`;
                    historyListContainer.insertAdjacentHTML('beforeend', txHTML);
                });
            }
        } else {
            console.error("Failed to fetch transactions");
        }
    } catch (error) {
        console.error("Server Error:", error);
    }
}



// Toggle between User ID and Mobile Number fields
function toggleReceiverFields() {
    const sendType = document.getElementById('sendType').value;
    const userIdGroup = document.getElementById('userIdGroup');
    const mobileGroup = document.getElementById('mobileGroup');
    const sendReceiver = document.getElementById('sendReceiver');
    const sendMobileNumber = document.getElementById('sendMobileNumber');

    if (sendType === 'user_id') {
        userIdGroup.style.display = 'block';
        mobileGroup.style.display = 'none';
        sendReceiver.required = true;
        sendMobileNumber.required = false;
    } else {
        userIdGroup.style.display = 'none';
        mobileGroup.style.display = 'block';
        sendReceiver.required = false;
        sendMobileNumber.required = true;
    }
}

//function for handling sending money
const sendMoney=document.getElementById('sendMoneyForm')
sendMoney.addEventListener('submit',async(e)=>{
    e.preventDefault()

    const sendType = document.getElementById('sendType').value;
    const amount = parseFloat(document.getElementById('sendAmount').value);
    const paymentMethod = document.getElementById('sendMethod').value;
    const description = document.getElementById('sendDescription').value;

    let endpoint = "http://localhost:8000/payment/payment_send";
    let payload;

    if (sendType === 'user_id') {
        // Send by User ID
        payload = {
            receiver_id: document.getElementById('sendReceiver').value,
            amount: amount,
            payment_method: paymentMethod,
            description: description
        };
    } else {
        // Send by Mobile Number (UPI)
        endpoint = "http://localhost:8000/payment/upi_send";
        payload = {
            receiver_number: parseInt(document.getElementById('sendMobileNumber').value),
            amount: amount,
            payment_method: paymentMethod,
            description: description
        };
    }

    try {
        const res=await fetch(endpoint,{
            method:"POST",
            headers:{
                'Authorization':`Bearer ${token}`,
                'Content-type':'application/json'
            },
            body:JSON.stringify(payload)
        })

        if (res.ok){
            const result=await res.json()
            alert("Payment Successful! Txn ID: " + result.txn_id);
            console.log(result);
            
            sendMoney.reset(); 
            document.getElementById('sendModal').classList.remove('active'); 
            document.getElementById('sendType').value = 'user_id';
            toggleReceiverFields();
            
            loadTransactions(); 
            loadBalance(); 
        }
        else{
            const errorData=await res.json()
            console.log(errorData);

            alert("Payment Failed: " + (errorData.detail || "Unknown Error"));
        }
    } catch (error) {
        console.error("Connection Error:", error);
        alert("Server is down. Please try again later.");
    }
})

async function loadBalance(){
    try {
       const res=await fetch("http://localhost:8000/wallet/check_balance",{
        headers:{
            "Authorization":`Bearer ${token}`
        }
       }) ;
       if(!res.ok){
            throw new Error("Failed to load balance");
       }

       const data=await res.json()
       if(data){
        console.log(data);
        
        document.querySelector('.balance').innerText = `₹${data}`;
       }

    } catch (error) {
        console.error(err);
        alert("Unable to load balance");
    }
}


// Call the function when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Ensure modals are direct children of <body> so `position: fixed` is viewport-relative
    document.querySelectorAll('.modal-overlay').forEach(modalEl => {
        if (modalEl.parentElement !== document.body) {
            document.body.appendChild(modalEl);
        }
    });

    loadBalance();
    loadTransactions();
    loadProfile();
});
