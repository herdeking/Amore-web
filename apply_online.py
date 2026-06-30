import re
path = 'index.html'
with open(path, 'r') as f:
    content = f.read()

old = """      <img src="${(other&&other.photos&&other.photos[0])||'https://placehold.co/40'}" style="width:40px;height:40px;border-radius:20px;object-fit:cover">
      <span style="font-size:16px;font-weight:700">${(other&&other.name)||'User'}</span>
    </div>"""

new = """      <img src="${(other&&other.photos&&other.photos[0])||'https://placehold.co/40'}" style="width:40px;height:40px;border-radius:20px;object-fit:cover">
      <div>
        <div style="font-size:16px;font-weight:700">${(other&&other.name)||'User'}</div>
        <div id="chatOnlineStatus" style="font-size:11px;color:#888">${(other&&other.isOnline)?'\u25CF Online':'Offline'}</div>
      </div>
    </div>"""

content = content.replace(old, new)
with open(path, 'w') as f:
    f.write(content)
print("✅ Online status added, replaced:", old in content)
