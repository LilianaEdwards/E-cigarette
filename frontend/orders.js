const API = "http://127.0.0.1:5000";

async function renderOrders() {
  try {
    const res = await fetch(`/orders`);
    const orders = await res.json();
    const tbody = document.querySelector("#orderTable tbody");
    tbody.innerHTML = "";

    if (!orders.length) {
      tbody.innerHTML = "<tr><td colspan='5'>No orders yet</td></tr>";
      return;
    }

    orders.forEach(o => {
      const items = o.items.map(i => `${i.name} x${i.qty}`).join(", ");
      tbody.innerHTML += `
        <tr>
          <td>${o.id}</td>
          <td>${o.date}</td>
          <td>${items}</td>
          <td>${o.total} MMK</td>
          <td>${o.status}</td>
        </tr>
      `;
    });

  } catch(err){ console.error(err); }
}
window.onload = renderOrders;

document.addEventListener("DOMContentLoaded", renderOrders);

