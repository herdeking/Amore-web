import re
path = 'index.html'
with open(path, 'r') as f:
    content = f.read()

old = """onAuthStateChanged(auth, async (user) => {
  if (user) {
    showPage('loadingPage');"""

new = """onAuthStateChanged(auth, async (user) => {
  if (user) {
    showPage('loadingPage');
    // Mark online
    updateDoc(doc(db, 'users', user.uid), { isOnline: true, lastSeen: new Date().toISOString() }).catch(function(){});
    window.addEventListener('beforeunload', function() {
      updateDoc(doc(db, 'users', user.uid), { isOnline: false, lastSeen: new Date().toISOString() }).catch(function(){});
    });"""

content = content.replace(old, new)
with open(path, 'w') as f:
    f.write(content)
print("✅ Set online status added, replaced:", old in content)
