const API = "http://127.0.0.1:5000";

async function renderCart() {
  try {
    const res = await fetch(`/cart`);
    const cartItems = await res.json();
    const tbody = document.querySelector("#cartTable tbody");
    const totalEl = document.getElementById("cart-total");
    tbody.innerHTML = "";
    let cartTotal = 0;

    if (!cartItems.length) {
      tbody.innerHTML = "<tr><td colspan='6'>Cart is empty</td></tr>";
      totalEl.innerText = "0";
      return;
    }

    cartItems.forEach(item => {
      const itemTotal = item.price*item.qty;
      cartTotal += itemTotal;

      tbody.innerHTML += `
      <tr>
        <td><img src="${item.img}" class="cart-img"></td>
        <td>${item.name}</td>
        <td>${item.price}</td>
        <td>${item.qty}</td>
        <td>${itemTotal}</td>
        <td><button class="btn danger" onclick="removeFromCart(${item.id})">Remove</button></td>
      </tr>`;
    });

    totalEl.innerText = cartTotal;
  } catch(err){console.error(err);}
}

async function removeFromCart(id){
  await fetch(`/cart/remove/${id}`, {method:"POST"});
  renderCart();
}

async function checkout(){
  // ✅ Get cart data EXACTLY how your app already stores it
  const items = JSON.parse(localStorage.getItem("cart")) || [];
  const total = items.reduce((sum, item) => sum + item.price * item.qty, 0);

  const res = await fetch(`/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      items: items,
      total: total
    })
  });

  const result = await res.json();

  if(result.message){
    alert("Order placed successfully!");
    localStorage.removeItem("cart"); // clear cart AFTER success
    renderCart();
  } else {
    alert(result.message || "Checkout failed");
  }
}

document.addEventListener("DOMContentLoaded", renderCart);







