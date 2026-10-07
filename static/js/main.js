const chatBox = document.getElementById("chatBox");
const chatToggle = document.getElementById("chatToggle");
if (chatToggle) chatToggle.addEventListener("click", toggleChat);

function toggleChat() {
  chatBox.classList.toggle("hidden");
  if (!chatBox.classList.contains("hidden")) document.getElementById("chatInput").focus();
}
async function sendChat() {
  const input = document.getElementById("chatInput");
  const msg = input.value.trim();
  if (!msg) return;
  const box = document.getElementById("chatMessages");
  box.innerHTML += `<div class="user bubble">${escapeHtml(msg)}</div>`;
  input.value = "";
  const loading = document.createElement("div");
  loading.className = "bot bubble";
  loading.textContent = "Đang tư vấn...";
  box.appendChild(loading);
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({message: msg})
    });
    const data = await res.json();
    loading.remove();
    box.innerHTML += `<div class="bot bubble">${escapeHtml(data.reply)}</div>`;
    if (data.products?.length) {
      data.products.forEach(p => {
        box.innerHTML += `<a class="chat-product" href="/product/${p.id}">
          <b>${escapeHtml(p.name)}</b><br><span>${Number(p.price).toLocaleString("vi-VN")}đ · ⭐ ${p.rating}</span>
        </a>`;
      });
    }
    box.scrollTop = box.scrollHeight;
  } catch (e) {
    loading.textContent = "Xin lỗi, chatbot đang gặp lỗi.";
  }
}
function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
document.addEventListener("keydown", e => {
  if (e.key === "Enter" && document.activeElement?.id === "chatInput") sendChat();
});

function openChatWith(productName) {
  if (typeof chatBox !== "undefined" && chatBox) chatBox.classList.remove("hidden");
  const input = document.getElementById("chatInput");
  if (input) {
    input.value = "Bạn tư vấn giúp tôi về " + productName + " và sản phẩm tương tự";
    input.focus();
  }
}
