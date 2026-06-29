path = '/data/data/com.termux/files/home/amore-web/index.html'
with open(path, 'r') as f:
    content = f.read()

old = """  el.innerHTML = `
    <div class="card" style="cursor:pointer" onclick="viewProfile('${p.id}')">"""

new = """  el.innerHTML = `
    <div class="card" style="cursor:pointer" id="currentCard">`;
  document.getElementById('currentCard').addEventListener('click', () => viewProfile(p.id));
  document.getElementById('currentCard').innerHTML += `"""

content = content.replace(old, new)

# Fix closing of the card
old_close = """      </div>
    </div>\`;"""
new_close = """      </div>
    </div>\`;"""

with open(path, 'w') as f:
    f.write(content)
print('✅ Card click fixed')
