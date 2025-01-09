document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const url = `/add_to_cart/${productId}`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                displayFlashMessage(data.status, data.message);

                if (data.status === 'success') {
                    // Fetch updated cart count
                    updateCartCount();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

function displayFlashMessage(status, message) {
    alert(message);

    const flashContainer = document.getElementById('flash-messages');
    const flashMessage = document.createElement('div');
    flashMessage.className = `alert alert-${status}`;
    flashMessage.textContent = message;

    flashContainer.appendChild(flashMessage);

    setTimeout(() => {
        flashMessage.remove();
    }, 3000);
}

function updateCartCount() {
    const cartCountElement = document.querySelector('.cart-count');  // Assuming your cart count is inside <span class="cart-count">
    
    fetch('/cart_count', {  // New endpoint to get the cart count
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.count !== undefined) {
            cartCountElement.textContent = data.count;  // Update the cart count on the page
        }
    })
    .catch(error => console.error('Error updating cart count:', error));
}
