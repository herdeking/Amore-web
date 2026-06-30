import re
path = 'index.html'
with open(path, 'r') as f:
    content = f.read()

old = """      <button class="btn btn-primary" style="margin-top:24px" onclick="openEditProfile()">Edit Profile</button>
      <button class="btn btn-outline" style="margin-top:8px" onclick="logout()">Log Out</button>
    </div>`;
}"""

new = """      <button class="btn btn-primary" style="margin-top:24px" onclick="document.getElementById('photoUploadInput').click()">\U0001F4F7 Add Photo</button>
      <input type="file" id="photoUploadInput" accept="image/*" style="display:none" onchange="uploadProfilePhoto(this)">
      <button class="btn btn-outline" style="margin-top:8px" onclick="openEditProfile()">Edit Profile</button>
      <button class="btn btn-outline" style="margin-top:8px" onclick="logout()">Log Out</button>
    </div>`;
}

window.uploadProfilePhoto = async function(input) {
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
};

window.deletePhoto = async function(idx) {
  if (!confirm('Remove this photo?')) return;
  try {
    const photos = (currentUser.photos || []).filter(function(p, i) { return i !== idx; });
    await updateDoc(doc(db, 'users', currentUser.id), { photos });
    currentUser.photos = photos;
    loadProfile();
    toast('Photo removed');
  } catch(e) { toast('Error: ' + e.message); }
};"""

content = content.replace(old, new)
with open(path, 'w') as f:
    f.write(content)
print("✅ Photo upload added, replaced:", old in content)
