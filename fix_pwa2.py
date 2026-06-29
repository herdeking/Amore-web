path = '/data/data/com.termux/files/home/amore-web/index.html'
with open(path, 'r') as f:
    content = f.read()

# Add auth persistence
old_import = "import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, sendPasswordResetEmail, onAuthStateChanged, signOut } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js';"
new_import = "import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, sendPasswordResetEmail, onAuthStateChanged, signOut, browserLocalPersistence, setPersistence } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js';"
content = content.replace(old_import, new_import)

# Set persistence after auth init
old_auth = "const auth = getAuth(app);"
new_auth = """const auth = getAuth(app);
setPersistence(auth, browserLocalPersistence).catch(() => {});"""
content = content.replace(old_auth, new_auth)

# Fix profile to show more details
old_profile_render = """  el.innerHTML = `
    <div class="profile-header">
      <img class="profile-cover" src="${currentUser.photos?.[0] ?? 'https://via.placeholder.com/480x250'}" onerror="this.src='https://via.placeholder.com/480x250'">
      <img class="profile-avatar" src="${currentUser.photos?.[0] ?? 'https://via.placeholder.com/90'}" onerror="this.src='https://via.placeholder.com/90'">
    </div>
    <div class="profile-body">
      <div class="profile-name">${currentUser.name ?? 'User'}</div>
      <div class="profile-location">📍 ${currentUser.location ?? 'Location not set'}</div>
      <p style="margin-top:12px;color:#555;font-size:14px">${currentUser.bio ?? 'No bio yet'}</p>
      <button class="btn btn-primary" style="margin-top:24px" onclick="logout()">Log Out</button>
    </div>`;"""

new_profile_render = """  el.innerHTML = `
    <div class="profile-header">
      <img class="profile-cover" src="${currentUser.photos?.[0] ?? 'https://via.placeholder.com/480x250'}" onerror="this.src='https://via.placeholder.com/480x250'" style="width:100%;height:250px;object-fit:cover">
      <img class="profile-avatar" src="${currentUser.photos?.[0] ?? 'https://via.placeholder.com/90'}" onerror="this.src='https://via.placeholder.com/90'" style="width:90px;height:90px;border-radius:45px;border:3px solid #fff;position:absolute;bottom:-45px;left:50%;transform:translateX(-50%);object-fit:cover">
    </div>
    <div class="profile-body">
      <div class="profile-name">${currentUser.name ?? 'User'}${currentUser.age ? ', ' + currentUser.age : ''}</div>
      <div class="profile-location">📍 ${currentUser.location ?? 'Location not set'}</div>
      <p style="margin-top:12px;color:#555;font-size:14px">${currentUser.bio ?? 'No bio yet'}</p>
      ${currentUser.interests?.length ? `<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">${currentUser.interests.map(i => `<span style="background:#fff0f3;color:#FF4B6E;padding:4px 12px;border-radius:20px;font-size:13px">${i}</span>`).join('')}</div>` : ''}
      <div style="margin-top:16px;background:#f8f8f8;border-radius:12px;padding:16px">
        ${currentUser.gender ? `<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #eee"><span style="color:#888">Gender</span><span style="font-weight:600">${currentUser.gender}</span></div>` : ''}
        ${currentUser.education ? `<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #eee"><span style="color:#888">Education</span><span style="font-weight:600">${currentUser.education}</span></div>` : ''}
        ${currentUser.height ? `<div style="display:flex;justify-content:space-between;padding:8px 0"><span style="color:#888">Height</span><span style="font-weight:600">${currentUser.height} cm</span></div>` : ''}
      </div>
      <button class="btn btn-primary" style="margin-top:24px" onclick="logout()">Log Out</button>
    </div>`;"""

content = content.replace(old_profile_render, new_profile_render)

with open(path, 'w') as f:
    f.write(content)
print('✅ Auth persistence and full profile fixed')
