const API = "http://127.0.0.1:5000";
const productGrid = document.getElementById("productGrid");

// Load products from backend
async function renderProducts() {
  try {
    const res = await fetch(`/products`);
    const products = await res.json();

    productGrid.innerHTML = "";

    products.forEach(p => {
      const card = document.createElement("div");
      card.className = `product-card ${p.stock === 0 ? "disabled" : ""}`;

      card.innerHTML = `
        <img src="${p.img}" alt="${p.name}" class="product-img">
        <h3>${p.name}</h3>
        <p class="price">${p.price} MMK</p>
        ${
          p.stock === 1
            ? `<button class="btn gold" onclick="addToCart(${p.id})">
                 Add to Cart
               </button>`
            : `<span class="out">OUT OF STOCK</span>`
        }
      `;

      productGrid.appendChild(card);
    });

  } catch (err) {
    console.error("Error loading products:", err);
    productGrid.innerHTML = "<p style='color:red'>Failed to load products</p>";
  }
}

// Add product to cart (backend)
async function addToCart(productId) {
  try {
    const res = await fetch(`${API}/products`);
    const products = await res.json();
    const product = products.find(p => p.id === productId);

    if (!product || product.stock === 0) {
      alert("Product is out of stock");
      return;
    }

    await fetch(`${API}/cart/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: product.id, name: product.name, price: product.price, qty: 1 })
    });

    alert("Added to cart");
  } catch (err) {
    console.error(err);
    alert("Failed to add to cart");
  }
}