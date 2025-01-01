// script.js
// Load products when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', fetchProducts);

const apiUrl = 'http://127.0.0.1:5001/api/products'; // Replace with your API URL

async function fetchProducts() {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const products = await response.json();
        renderProducts(products);
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// function renderProducts(products) {
//     const container = document.getElementById('product-container');
//     container.innerHTML = ''; // Clear existing content

//     products.forEach(product => {
//         // Create a product card
//         const productDiv = document.createElement('div');
//         productDiv.className = 'product';

//         // Populate product details
//         productDiv.innerHTML = `
//             <h3>${product.name}</h3>
//             <p>Price: $${product.price}</p>
//             <img src="${product.image}" alt="${product.name}" width="150">
//             <button>Add to Cart</button>
//         `;

//         // Append to container
//         container.appendChild(productDiv);
//     });
// }

function renderProducts(products) {
    // Select the container (correcting class selection)
    const container = document.querySelector('.products_container');
    container.innerHTML = ''; // Clear existing content

    products.forEach(product => {
        // Create a product card dynamically
        const productDiv = document.createElement('div');
        productDiv.className = 'product';

        // Populate product details (fixing tags)
        productDiv.innerHTML = `
            <img src="images/product.png" alt="${product.name}">
            <div class="description">
                <span>Brand Name</span>
                <h5>${product.name}</h5>
                <div class="star">
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                </div>
                <h4>$${product.price}</h4>
            </div>
            <a href="#">
                <i class="fas fa-shopping-cart cart"></i>
            </a>
        `;

        // Append the product card to the container
        container.appendChild(productDiv);
    });
}

