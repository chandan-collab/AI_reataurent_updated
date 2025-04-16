// Function to show popup messages
function showPopup(message, type = 'success') {
    const popup = document.createElement('div');
    popup.classList.add('popup');

    // Style the popup based on type
    popup.style.position = 'fixed';
    popup.style.top = '50%';
    popup.style.left = '50%';
    popup.style.transform = 'translate(-50%, -50%)';
    popup.style.padding = '20px';
    popup.style.borderRadius = '8px';
    popup.style.zIndex = '1000';
    popup.style.color = '#fff';
    popup.style.fontSize = '18px';
    popup.style.fontWeight = 'bold';
    popup.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.3)';
    popup.style.animation = 'fadeIn 0.5s';

    // Set colors based on action type
    if (type === 'success') {
        popup.style.backgroundColor = '#28a745';  // Green for success
    } else if (type === 'error') {
        popup.style.backgroundColor = '#dc3545';  // Red for error
    } else if (type === 'warning') {
        popup.style.backgroundColor = '#ffc107';  // Yellow for warning
        popup.style.color = '#000';
    }

    popup.textContent = message;

    // Add the popup to the body
    document.body.appendChild(popup);

    // Remove popup after 3 seconds
    setTimeout(() => {
        popup.remove();
    }, 3000);
}

// Event listeners for actions
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    
    // Check for query parameters to trigger popups
    if (urlParams.has('insert') && urlParams.get('insert') === 'success') {
        showPopup('Menu item added successfully!', 'success');
    }
    
    if (urlParams.has('delete') && urlParams.get('delete') === 'success') {
        showPopup('Menu item deleted successfully!', 'error');
    }

    if (urlParams.has('edit') && urlParams.get('edit') === 'success') {
        showPopup('Menu item updated successfully!', 'success');
    }
});
