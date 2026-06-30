import re
path = 'index.html'
with open(path, 'r') as f:
    content = f.read()

old = """      <div style="display:flex;gap:12px;margin-top:24px">
        <button class="btn btn-primary" onclick="swipeLike();this.closest('div[style*=fixed]').remove()">\u2764\uFE0F Like</button>
        <button class="btn btn-outline" onclick="this.closest('div[style*=fixed]').remove()">Skip</button>
      </div>
    </div>`;
  document.body.appendChild(modal);
};"""

new = """      <div style="display:flex;gap:12px;margin-top:24px">
        <button class="btn btn-primary" onclick="swipeLike();this.closest('div[style*=fixed]').remove()">\u2764\uFE0F Like</button>
        <button class="btn btn-outline" onclick="startChatFrom('${p.id}')">\U0001F4AC Message</button>
      </div>
      <button class="btn btn-outline" style="margin-top:8px" onclick="this.closest('div[style*=fixed]').remove()">Skip</button>
    </div>`;
  document.body.appendChild(modal);
};

window.startChatFrom = async function(otherId) {
  try {
    const q = query(collection(db, 'matches'), where('users', 'array-contains', currentUser.id));
    const snap = await getDocs(q);
    let matchId = null;
    snap.forEach(function(d) {
      if (d.data().users.includes(otherId)) matchId = d.id;
    });
    if (!matchId) {
      const ref = await addDoc(collection(db, 'matches'), {
        users: [currentUser.id, otherId],
        createdAt: new Date().toISOString(),
      });
      matchId = ref.id;
    }
    document.querySelectorAll('div[style*=fixed]').forEach(function(m){ m.remove(); });
    switchTab('messagesTab', document.querySelectorAll('.nav-item')[2]);
    toast('Match created! Find them in Messages.');
  } catch(e) { toast('Error: ' + e.message); }
};"""

content = content.replace(old, new)
with open(path, 'w') as f:
    f.write(content)
print("✅ Chat button added, replaced:", old in content)
