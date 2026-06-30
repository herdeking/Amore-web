import re
path = 'index.html'
with open(path, 'r') as f:
    content = f.read()

old = """window.viewProfile = (userId) => {
  const p = profiles.find(u => u.id === userId);
  if (!p) return;
  const modal = document.createElement('div');
  modal.style.cssText = 'position:fixed;inset:0;background:#fff;z-index:999;overflow-y:auto;max-width:480px;margin:0 auto';
  modal.innerHTML = `
    <div style="position:sticky;top:0;background:#fff;padding:16px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #eee;z-index:1">
      <span onclick="this.closest('div[style*=fixed]').remove()" style="font-size:28px;cursor:pointer">\u2039</span>
      <span style="font-size:18px;font-weight:700">${p.name ?? 'Profile'}</span>
    </div>
    <img src="${p.photos?.[0] ?? 'https://placehold.co/480x400'}" style="width:100%;height:400px;object-fit:cover">
    <div style="padding:20px">
      <div style="font-size:24px;font-weight:800">${p.name ?? 'Unknown'}${p.age ? ', ' + p.age : ''}</div>
      <div style="color:#888;margin-top:4px">\U0001F4CD ${p.location ?? ''}</div>
      ${p.bio ? `<p style="margin-top:12px;color:#555">${p.bio}</p>` : ''}
      ${p.interests?.length ? `<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">${p.interests.map(i=>`<span style="background:#fff0f3;color:#FF4B6E;padding:4px 12px;border-radius:20px;font-size:13px">${i}</span>`).join('')}</div>` : ''}
      <div style="display:flex;gap:12px;margin-top:24px">
        <button class="btn btn-primary" onclick="swipeLike();this.closest('div[style*=fixed]').remove()">\u2764\uFE0F Like</button>
        <button class="btn btn-outline" onclick="this.closest('div[style*=fixed]').remove()">Skip</button>
      </div>
    </div>`;
  document.body.appendChild(modal);
};"""

new = """window.viewProfile = (userId) => {
  const p = profiles.find(u => u.id === userId);
  if (!p) return;
  const photos = p.photos ?? [];
  const modal = document.createElement('div');
  modal.style.cssText = 'position:fixed;inset:0;background:#fff;z-index:999;overflow-y:auto;max-width:480px;margin:0 auto';
  modal.innerHTML = `
    <div style="position:sticky;top:0;background:#fff;padding:16px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #eee;z-index:1">
      <span onclick="this.closest('div[style*=fixed]').remove()" style="font-size:28px;cursor:pointer">\u2039</span>
      <span style="font-size:18px;font-weight:700">${p.name ?? 'Profile'}</span>
    </div>
    <img src="${photos[0] ?? 'https://placehold.co/480x400'}" style="width:100%;height:400px;object-fit:cover">
    <div style="padding:20px">
      <div style="font-size:24px;font-weight:800">${p.name ?? 'Unknown'}${p.age ? ', ' + p.age : ''}</div>
      <div style="color:#888;margin-top:4px">\U0001F4CD ${p.location ?? ''}</div>
      ${p.bio ? `<p style="margin-top:12px;color:#555">${p.bio}</p>` : ''}
      ${p.interests?.length ? `<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">${p.interests.map(function(i){return `<span style="background:#fff0f3;color:#FF4B6E;padding:4px 12px;border-radius:20px;font-size:13px">${i}</span>`;}).join('')}</div>` : ''}
      <div style="margin-top:16px;background:#f8f8f8;border-radius:16px;padding:16px">
        <div style="font-weight:700;margin-bottom:12px">About</div>
        ${[['Gender',p.gender],['Purpose',p.purpose],['Height',p.height?p.height+' cm':null],['Weight',p.weight?p.weight+' kg':null],['Education',p.education],['Smoking',p.smoking],['Alcohol',p.alcohol],['Children',p.children],['Physique',p.physique],['Dwelling',p.dwelling],['Car',p.car],['Sociability',p.sociability],['Looking for',p.lookingFor]].filter(function(f){return f[1];}).map(function(f){return `<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #eee"><span style="color:#888">${f[0]}</span><span style="font-weight:600">${f[1]}</span></div>`;}).join('')}
      </div>
      ${photos.length > 1 ? `<div style="margin-top:20px"><div style="font-weight:700;margin-bottom:12px">Photos (${photos.length})</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px">${photos.map(function(ph){return `<img src="${ph}" style="width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px;cursor:pointer" onclick="viewPhotoFull('${ph}')" onerror="this.style.display='none'">`;}).join('')}</div></div>` : ''}
      <div style="display:flex;gap:12px;margin-top:24px">
        <button class="btn btn-primary" onclick="swipeLike();this.closest('div[style*=fixed]').remove()">\u2764\uFE0F Like</button>
        <button class="btn btn-outline" onclick="this.closest('div[style*=fixed]').remove()">Skip</button>
      </div>
    </div>`;
  document.body.appendChild(modal);
};"""

content = content.replace(old, new)
with open(path, 'w') as f:
    f.write(content)
print("✅ View profile enhanced, contains old:", old in content)
