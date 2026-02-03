const API = "http://127.0.0.1:5000";

// ----------------------
// Tab controls
// ----------------------
function showOrders(){
  document.getElementById("ordersTableDiv").style.display = "block";
  document.getElementById("stockTableDiv").style.display = "none";
  document.querySelectorAll(".tab-btn")[0].classList.add("active");
  document.querySelectorAll(".tab-btn")[1].classList.remove("active");
  renderOrdersAdmin();
}

function showStock(){
  document.getElementById("ordersTableDiv").style.display = "none";
  document.getElementById("stockTableDiv").style.display = "block";
  document.querySelectorAll(".tab-btn")[1].classList.add("active");
  document.querySelectorAll(".tab-btn")[0].classList.remove("active");
  renderStock();
}

// ----------------------
// Render Orders Table
// ----------------------
async function renderOrdersAdmin() {
  try {
    const res = await fetch(`/orders`);
    const orders = await res.json();
    const tbody = document.querySelector("#adminOrderTable tbody");
    tbody.innerHTML = "";

    if(!orders.length){
      tbody.innerHTML = "<tr><td colspan='6'>No orders yet</td></tr>";
      return;
    }

    orders.forEach(o => {
      const items = o.items.map(i=>`${i.name} x${i.qty}`).join(", ");
      tbody.innerHTML += `
        <tr>
          <td>${o.id}</td>
          <td>${o.date}</td>
          <td>${items}</td>
          <td>${o.total}</td>
          <td>${o.status}</td>
          <td>
            <button class="btn gold" onclick="updateStatus(${o.id},'APPROVED')">Approve</button>
            <button class="btn danger" onclick="updateStatus(${o.id},'REJECTED')">Reject</button>
          </td>
        </tr>
      `;
    });
  } catch(err){ console.error(err); }
}

// ----------------------
// Render Stock Table
// ----------------------
async function renderStock() {
  try {
    const res = await fetch(`${API}/products`);
    const products = await res.json();
    const tbody = document.querySelector("#stockTable tbody");
    tbody.innerHTML = "";

    products.forEach(p => {
      tbody.innerHTML += `
        <tr>
          <td>${p.name}</td>
          <td>${p.price}</td>
          <td>${p.stock ? "IN STOCK":"OUT OF STOCK"}</td>
          <td>
            <button class="btn gold" onclick="toggleStock(${p.id})">
              ${p.stock ? "Set Out of Stock":"Set In Stock"}
            </button>
          </td>
        </tr>
      `;
    });
  } catch(err){ console.error(err); }
}

// ----------------------
// Stock toggle
// ----------------------
async function toggleStock(pid){
  try {
    await fetch(`${API}/stock/toggle/${pid}`, {method:"POST"});
    renderStock();
    renderProducts(); // refresh user products
  } catch(err){ console.error(err); }
}

// ----------------------
// Order approve/reject
// ----------------------
async function updateStatus(oid, status){
  try {
    await fetch(`${API}/order/status/${oid}`, {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({status})
    });
    renderOrdersAdmin();
  } catch(err){ console.error(err); }
}