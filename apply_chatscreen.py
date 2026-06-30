import re
path = 'index.html'
with open(path, 'r') as f:
    content = f.read()

old = """window.openChat = (matchId, otherId) => {
  toast('Chat coming soon!');
};"""

new = """let chatUnsub = null;

window.openChat = async function(matchId, otherId) {
  const otherSnap = await getDoc(doc(db, 'users', otherId));
  const other = otherSnap.data();
  const modal = document.createElement('div');
  modal.id = 'chatModal';
  modal.style.cssText = 'position:fixed;inset:0;background:#f0f0f0;z-index:999;max-width:480px;margin:0 auto;display:flex;flex-direction:column';
  modal.innerHTML = `
    <div style="background:#fff;padding:16px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #eee">
      <span onclick="closeChatModal()" style="font-size:28px;cursor:pointer">\u2039</span>
      <img src="${(other&&other.photos&&other.photos[0])||'https://placehold.co/40'}" style="width:40px;height:40px;border-radius:20px;object-fit:cover">
      <span style="font-size:16px;font-weight:700">${(other&&other.name)||'User'}</span>
    </div>
    <div id="chatMessages" style="flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:8px"></div>
    <div style="background:#fff;padding:12px;display:flex;gap:8px;border-top:1px solid #eee">
      <input id="chatInput" class="input" placeholder="Type a message..." style="margin:0" onkeypress="if(event.key==='Enter')sendChatMsg('${matchId}')">
      <button onclick="sendChatMsg('${matchId}')" style="background:#FF4B6E;color:#fff;border:none;border-radius:20px;padding:0 20px;font-weight:700">Send</button>
    </div>`;
  document.body.appendChild(modal);

  const q = query(collection(db, 'matches', matchId, 'messages'), orderBy('createdAt', 'asc'));
  if (chatUnsub) chatUnsub();
  chatUnsub = onSnapshot(q, function(snap) {
    const el = document.getElementById('chatMessages');
    if (!el) return;
    el.innerHTML = snap.docs.map(function(d) {
      const m = d.data();
      const mine = m.senderId === currentUser.id;
      return `<div style="align-self:${mine?'flex-end':'flex-start'};background:${mine?'#FF4B6E':'#fff'};color:${mine?'#fff':'#333'};padding:10px 14px;border-radius:16px;max-width:75%;font-size:14px">${m.text}</div>`;
    }).join('');
    el.scrollTop = el.scrollHeight;
  });
};

window.closeChatModal = function() {
  if (chatUnsub) { chatUnsub(); chatUnsub = null; }
  const m = document.getElementById('chatModal');
  if (m) m.remove();
};

window.sendChatMsg = async function(matchId) {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  try {
    await addDoc(collection(db, 'matches', matchId, 'messages'), {
      senderId: currentUser.id,
      text,
      createdAt: new Date().toISOString(),
      read: false,
    });
    await updateDoc(doc(db, 'matches', matchId), {
      lastMessage: text,
      lastMessageTime: new Date().toISOString(),
    });
  } catch(e) { toast('Error: ' + e.message); }
};"""

content = content.replace(old, new)
with open(path, 'w') as f:
    f.write(content)
print("✅ Chat screen added, replaced:", old in content)
