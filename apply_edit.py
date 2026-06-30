import re
path = 'index.html'
with open(path, 'r') as f:
    content = f.read()
marker = "window.openEditProfile = function() {"
end_marker = "window.saveProfile = async function() {"
start = content.index(marker)
end_func_start = content.index(end_marker)
after_save = content[end_func_start:]
catch_idx = after_save.index("catch(e)")
close_idx = after_save.index("};", catch_idx) + 2
end = end_func_start + close_idx
helpers = """function selField(id, label, val, options) {
  return `<label style="font-size:13px;color:#888;font-weight:600;display:block;margin-top:14px">${label}</label>
    <select class="input" id="${id}" style="margin-top:6px">
      <option value="">Select</option>
      ${options.map(function(o){return `<option value="${o}" ${val===o?'selected':''}>${o}</option>`;}).join('')}
    </select>`;
}
function txtField(id, label, val, type) {
  return `<label style="font-size:13px;color:#888;font-weight:600;display:block;margin-top:14px">${label}</label>
    <input class="input" id="${id}" type="${type||'text'}" value="${val||''}" style="margin-top:6px">`;
}

"""
new_func = """window.openEditProfile = function() {
  const u = currentUser;
  const modal = document.createElement('div');
  modal.id = 'editModal';
  modal.style.cssText = 'position:fixed;inset:0;background:#fff;z-index:999;overflow-y:auto;max-width:480px;margin:0 auto';
  modal.innerHTML = `
    <div style="position:sticky;top:0;background:#fff;padding:16px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #eee;z-index:1">
      <span onclick="document.getElementById('editModal').remove()" style="font-size:28px;cursor:pointer">\u2039</span>
      <span style="font-size:18px;font-weight:700">Edit Profile</span>
    </div>
    <div style="padding:20px 20px 40px">
      ${txtField('editName','Name',u.name)}
      ${selField('editGender','Gender',u.gender,['Male','Female'])}
      ${txtField('editDob','Birthday (YYYY-MM-DD)',u.dob,'text')}
      ${txtField('editLocation','Location',u.location)}
      <label style="font-size:13px;color:#888;font-weight:600;display:block;margin-top:14px">About me</label>
      <textarea class="input" id="editBio" rows="3" style="margin-top:6px;resize:vertical">${u.bio||''}</textarea>
      ${selField('editPurpose','Purpose',u.purpose,['Relationship','Friendship','Casual','Marriage'])}
      ${txtField('editHeight','Height (cm)',u.height,'number')}
      ${txtField('editWeight','Weight (kg)',u.weight,'number')}
      ${txtField('editEducation','Education',u.education)}
      ${selField('editSmoking','Smoking',u.smoking,['Never','Occasionally','Regularly'])}
      ${selField('editAlcohol','Alcohol',u.alcohol,['Never','Occasionally','Regularly'])}
      ${selField('editChildren','Children',u.children,['No children','Have children','Want children','Do not want'])}
      ${selField('editPhysique','Physique',u.physique,['Slim','Athletic','Average','Curvy','Plus size'])}
      ${selField('editDwelling','Dwelling',u.dwelling,['Apartment','House','With parents','Other'])}
      ${selField('editCar','Car',u.car,['No car','Have a car'])}
      ${selField('editSociability','Sociability',u.sociability,['Introvert','Extrovert','Ambivert'])}
      ${selField('editLookingFor','Looking for',u.lookingFor,['Man','Woman','Both','Everyone'])}
      ${txtField('editInterests','Interests (comma separated)',(u.interests||[]).join(', '))}
      <button class="btn btn-primary" style="margin-top:24px" onclick="saveProfile()">Save Changes</button>
    </div>`;
  document.body.appendChild(modal);
};
window.saveProfile = async function() {
  try {
    const g = function(id){ return document.getElementById(id).value; };
    const updates = {
      name: g('editName'),
      gender: g('editGender'),
      dob: g('editDob'),
      location: g('editLocation'),
      bio: g('editBio'),
      purpose: g('editPurpose'),
      height: parseInt(g('editHeight')) || null,
      weight: parseInt(g('editWeight')) || null,
      education: g('editEducation'),
      smoking: g('editSmoking'),
      alcohol: g('editAlcohol'),
      children: g('editChildren'),
      physique: g('editPhysique'),
      dwelling: g('editDwelling'),
      car: g('editCar'),
      sociability: g('editSociability'),
      lookingFor: g('editLookingFor'),
      interests: g('editInterests').split(',').map(function(s){return s.trim();}).filter(Boolean),
    };
    await updateDoc(doc(db, 'users', currentUser.id), updates);
    Object.assign(currentUser, updates);
    document.getElementById('editModal').remove();
    loadProfile();
    toast('Profile updated!');
  } catch(e) { toast('Error: ' + e.message); }
};"""

content = content[:start] + helpers + new_func + content[end:]
with open(path, 'w') as f:
    f.write(content)
print("✅ Full edit profile applied, new length:", len(content))
