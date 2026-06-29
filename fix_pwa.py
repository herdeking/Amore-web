path = '/data/data/com.termux/files/home/amore-web/index.html'
with open(path, 'r') as f:
    content = f.read()

# Fix profile - show name from auth if Firestore fails
old_profile = """onAuthStateChanged(auth, async (user) => {
  if (user) {
    const snap = await getDoc(doc(db, 'users', user.uid));
    currentUser = { id: user.uid, ...snap.data() };
    showPage('appPage');
    loadProfiles();
  } else {
    currentUser = null;
    showPage('loginPage');
  }
});"""

new_profile = """onAuthStateChanged(auth, async (user) => {
  if (user) {
    try {
      const snap = await getDoc(doc(db, 'users', user.uid));
      if (snap.exists()) {
        currentUser = { id: user.uid, ...snap.data() };
      } else {
        currentUser = { id: user.uid, name: user.displayName ?? user.email?.split('@')[0] ?? 'User', email: user.email, photos: [] };
      }
    } catch(e) {
      currentUser = { id: user.uid, name: user.email?.split('@')[0] ?? 'User', email: user.email, photos: [] };
    }
    showPage('appPage');
    switchTab('discoverTab', document.querySelector('.nav-item'));
    loadProfiles();
  } else {
    currentUser = null;
    showPage('loginPage');
  }
});"""

content = content.replace(old_profile, new_profile)

with open(path, 'w') as f:
    f.write(content)
print('✅ PWA auth fixed')
