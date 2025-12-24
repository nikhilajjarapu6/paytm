const sendBtn = document.querySelector('.send');
const modal = document.getElementById('sendModal');
const closeBtn = document.getElementById('closeModal');

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
editForm.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent page refresh

    // Get values from inputs
    const newName = document.getElementById('editName').value;
    const newUpi = document.getElementById('editUpi').value;
    const newEmail = document.getElementById('editEmail').value;

    // Update the Dashboard UI
    displayName.innerText = newName;
    displayUpi.innerText = newUpi;
    displayEmail.innerText = newEmail;

    // Success effect
    alert("Profile Updated Successfully!");
    
    // Close Modal
    editModal.classList.remove('active');
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