path = '/data/data/com.termux/files/home/amore-web/index.html'
with open(path, 'r') as f:
    content = f.read()

# Fix: filter out current user from profiles and load more
old_load = """    const snap = await getDocs(collection(db, 'users'));
    profiles = snap.docs
      .map(d => ({ id: d.id, ...d.data() }))
      .filter(u => u.id !== currentUser?.id && u.photos?.length > 0);"""

new_load = """    const snap = await getDocs(collection(db, 'users'));
    profiles = snap.docs
      .map(d => ({ id: d.id, ...d.data() }))
      .filter(u => u.id !== currentUser?.id && (u.photos?.length > 0 || u.photoURL));
    // Shuffle profiles
    profiles = profiles.sort(() => Math.random() - 0.5);"""

content = content.replace(old_load, new_load)

with open(path, 'w') as f:
    f.write(content)
print('✅ Fixed')
