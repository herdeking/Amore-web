import re
path = 'index.html'
with open(path, 'r') as f:
    content = f.read()

old = """window.uploadProfilePhoto = async function(input) {
  const file = input.files[0];
  if (!file) return;
  toast('Uploading photo...');
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', 'amore_simple');
    const res = await fetch('https://api.cloudinary.com/v1_1/danwexfev/image/upload', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    if (data.secure_url) {
      const photos = currentUser.photos || [];
      photos.push(data.secure_url);
      await updateDoc(doc(db, 'users', currentUser.id), { photos });
      currentUser.photos = photos;
      loadProfile();
      toast('Photo added!');
    } else {
      toast('Upload failed');
    }
  } catch(e) { toast('Error: ' + e.message); }
};"""

new = """window.uploadProfilePhoto = async function(input) {
  const file = input.files[0];
  if (!file) return;
  toast('Uploading photo...');
  let url = null;
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', 'amore_simple');
    const res = await fetch('https://api.cloudinary.com/v1_1/danwexfev/image/upload', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    if (data.secure_url) url = data.secure_url;
  } catch(e) {}

  if (!url) {
    try {
      const fd2 = new FormData();
      fd2.append('image', file);
      const res2 = await fetch('https://api.imgbb.com/1/upload?key=405b4c04088db65af0932530b5bf0420', {
        method: 'POST',
        body: fd2,
      });
      const data2 = await res2.json();
      if (data2.data && data2.data.url) url = data2.data.url;
    } catch(e) {}
  }

  if (url) {
    const photos = currentUser.photos || [];
    photos.push(url);
    await updateDoc(doc(db, 'users', currentUser.id), { photos });
    currentUser.photos = photos;
    loadProfile();
    toast('Photo added!');
  } else {
    toast('Upload failed - try again');
  }
};"""

content = content.replace(old, new)
with open(path, 'w') as f:
    f.write(content)
print("✅ imgbb fallback added, replaced:", old in content)
