document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("productSearch");
    const productCards = document.querySelectorAll(".product-card");

    const cartItemsContainer = document.getElementById("cartItems");
    const cartCount = document.getElementById("cartCount");
    const cartWeight = document.getElementById("cartWeight");
    const createOrderButton = document.getElementById("createOrder");
    const orderForm = document.getElementById("orderForm");

    const cart = {};


    function updateProductSearch() {

        const searchText = searchInput.value.toLowerCase().trim();

        productCards.forEach(card => {

            const name = card.dataset.productName || "";
            const sku = card.dataset.productSku || "";

            if (
                name.includes(searchText) ||
                sku.includes(searchText)
            ) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }

        });

    }


    function updateCart() {

        cartItemsContainer.innerHTML = "";

        const productIds = Object.keys(cart);

        if (productIds.length === 0) {

            cartItemsContainer.innerHTML = `
                <div class="cart-empty">
                    <div class="empty-icon">⌂</div>

                    <h3>Your order is empty</h3>

                    <p>
                        Select products from the warehouse to build an order.
                    </p>
                </div>
            `;

            cartCount.textContent = "0 items";
            cartWeight.textContent = "0 kg";
            createOrderButton.disabled = true;

            return;
        }


        let totalItems = 0;
        let totalWeight = 0;


        productIds.forEach(productId => {

            const item = cart[productId];

            totalItems += item.quantity;

            totalWeight += item.weight * item.quantity;


            const cartItem = document.createElement("div");

            cartItem.className = "cart-item";

            cartItem.innerHTML = `
                <div>
                    <strong>${item.name}</strong>

                    <span>
                        ${item.weight} kg each
                    </span>
                </div>

                <div class="cart-item-controls">

                    <button
                        type="button"
                        class="quantity-button"
                        data-action="decrease"
                        data-product-id="${productId}"
                    >
                        −
                    </button>

                    <span>
                        ${item.quantity}
                    </span>

                    <button
                        type="button"
                        class="quantity-button"
                        data-action="increase"
                        data-product-id="${productId}"
                    >
                        +
                    </button>

                </div>
            `;

            cartItemsContainer.appendChild(cartItem);

        });


        cartCount.textContent =
            `${totalItems} ${totalItems === 1 ? "item" : "items"}`;

        cartWeight.textContent =
            `${totalWeight.toFixed(2)} kg`;

        createOrderButton.disabled = false;

    }


    function addProduct(productId, name, weight) {

        if (cart[productId]) {

            cart[productId].quantity += 1;

        } else {

            cart[productId] = {
                id: productId,
                name: name,
                weight: Number(weight),
                quantity: 1
            };

        }

        updateCart();

    }


    function changeQuantity(productId, change) {

        if (!cart[productId]) {
            return;
        }

        cart[productId].quantity += change;


        if (cart[productId].quantity <= 0) {
            delete cart[productId];
        }

        updateCart();

    }


    document.querySelectorAll(".add-product").forEach(button => {

        button.addEventListener("click", () => {

            const productId = button.dataset.productId;
            const productName = button.dataset.productName;
            const productWeight = button.dataset.productWeight;

            addProduct(
                productId,
                productName,
                productWeight
            );

        });

    });


    cartItemsContainer.addEventListener("click", event => {

        const button = event.target.closest(".quantity-button");

        if (!button) {
            return;
        }

        const productId = button.dataset.productId;
        const action = button.dataset.action;

        if (action === "increase") {
            changeQuantity(productId, 1);
        }

        if (action === "decrease") {
            changeQuantity(productId, -1);
        }

    });


    if (searchInput) {
        searchInput.addEventListener(
            "input",
            updateProductSearch
        );
    }


    if (orderForm) {

        orderForm.addEventListener("submit", () => {

            Object.keys(cart).forEach(productId => {

                const productInput = document.createElement("input");

                productInput.type = "hidden";
                productInput.name = "product_id";
                productInput.value = productId;

                orderForm.appendChild(productInput);


                const quantityInput = document.createElement("input");

                quantityInput.type = "hidden";
                quantityInput.name = `quantity_${productId}`;
                quantityInput.value = cart[productId].quantity;

                orderForm.appendChild(quantityInput);

            });

        });

    }


    updateCart();

});