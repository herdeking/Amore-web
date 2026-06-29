path = '/data/data/com.termux/files/home/amore-web/index.html'
with open(path, 'r') as f:
    content = f.read()

# Fix showCard to be more robust and clickable
old_card = """function showCard() {
  const el = document.getElementById('swipeCards');
  if (profileIndex >= profiles.length) {
    el.innerHTML = '<div style="text-align:center;padding:60px 20px"><div style="font-size:48px">💫</div><p style="font-size:18px;font-weight:700;margin-top:16px">No more profiles!</p><p style="color:#888;margin-top:8px">Check back later</p></div>';
    return;
  }
  currentProfile = profiles[profileIndex];
  el.innerHTML = `
    <div class="card">
      <img class="card-img" src="${currentProfile.photos?.[0] ?? 'https://via.placeholder.com/400'}" onerror="this.src='https://via.placeholder.com/400'">
      <div class="card-info">
        <div class="card-name">${currentProfile.name ?? 'Unknown'}, ${currentProfile.age ?? ''}</div>
        <div class="card-location">📍 ${currentProfile.location ?? ''}</div>
        <div class="card-bio">${currentProfile.bio ?? ''}</div>
      </div>
    </div>`;
}"""

new_card = """function showCard() {
  const el = document.getElementById('swipeCards');
  if (profileIndex >= profiles.length) {
    el.innerHTML = '<div style="text-align:center;padding:60px 20px"><div style="font-size:48px">💫</div><p style="font-size:18px;font-weight:700;margin-top:16px">No more profiles!</p><p style="color:#888;margin-top:8px">Check back later</p><button class="btn btn-primary" style="width:auto;padding:12px 24px;margin-top:16px" onclick="loadProfiles()">Refresh</button></div>';
    return;
  }
  currentProfile = profiles[profileIndex];
  const p = currentProfile;
  el.innerHTML = `
    <div class="card" style="cursor:pointer" onclick="viewProfile('${p.id}')">
      <div style="position:relative">
        <img class="card-img" src="${p.photos?.[0] ?? 'https://placehold.co/400x500/FF4B6E/white?text=No+Photo'}" onerror="this.src='https://placehold.co/400x500/FF4B6E/white?text=No+Photo'" style="width:100%;height:450px;object-fit:cover">
        <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,0.7));padding:20px;color:#fff">
          <div style="font-size:24px;font-weight:800">${p.name ?? 'Unknown'}${p.age ? ', ' + p.age : ''}</div>
          <div style="font-size:13px;opacity:0.9;margin-top:4px">📍 ${p.location ?? 'Unknown location'}</div>
          ${p.bio ? `<div style="font-size:13px;opacity:0.8;margin-top:6px">${p.bio.substring(0,80)}${p.bio.length>80?'...':''}</div>` : ''}
        </div>
      </div>
    </div>`;
}

window.viewProfile = (userId) => {
  const p = profiles.find(u => u.id === userId);
  if (!p) return;
  const modal = document.createElement('div');
  modal.style.cssText = 'position:fixed;inset:0;background:#fff;z-index:999;overflow-y:auto;max-width:480px;margin:0 auto';
  modal.innerHTML = `
    <div style="position:sticky;top:0;background:#fff;padding:16px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #eee;z-index:1">
      <span onclick="this.closest('div[style*=fixed]').remove()" style="font-size:28px;cursor:pointer">‹</span>
      <span style="font-size:18px;font-weight:700">${p.name ?? 'Profile'}</span>
    </div>
    <img src="${p.photos?.[0] ?? 'https://placehold.co/480x400'}" style="width:100%;height:400px;object-fit:cover">
    <div style="padding:20px">
      <div style="font-size:24px;font-weight:800">${p.name ?? 'Unknown'}${p.age ? ', ' + p.age : ''}</div>
      <div style="color:#888;margin-top:4px">📍 ${p.location ?? ''}</div>
      ${p.bio ? `<p style="margin-top:12px;color:#555">${p.bio}</p>` : ''}
      ${p.interests?.length ? `<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">${p.interests.map(i=>`<span style="background:#fff0f3;color:#FF4B6E;padding:4px 12px;border-radius:20px;font-size:13px">${i}</span>`).join('')}</div>` : ''}
      <div style="display:flex;gap:12px;margin-top:24px">
        <button class="btn btn-primary" onclick="swipeLike();this.closest('div[style*=fixed]').remove()">❤️ Like</button>
        <button class="btn btn-outline" onclick="this.closest('div[style*=fixed]').remove()">Skip</button>
      </div>
    </div>`;
  document.body.appendChild(modal);
};"""

content = content.replace(old_card, new_card)

with open(path, 'w') as f:
    f.write(content)
print('✅ Swipe cards fixed')
