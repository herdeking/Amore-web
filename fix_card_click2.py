path = '/data/data/com.termux/files/home/amore-web/index.html'
with open(path, 'r') as f:
    content = f.read()

old = '    <div class="card" style="cursor:pointer" onclick="viewProfile(\'${p.id}\')">'
new = '    <div class="card" style="cursor:pointer" data-uid="${p.id}" id="swipeCard">'

content = content.replace(old, new)

# Add click listener after innerHTML
old_after = "window.viewProfile = (userId) => {"
new_after = """// Add click to card after render
const addCardClick = () => {
  const card = document.getElementById('swipeCard');
  if (card) card.onclick = () => viewProfile(card.dataset.uid);
};

window.viewProfile = (userId) => {"""
content = content.replace(old_after, new_after)

# Call addCardClick after showCard sets innerHTML
old_showcard_end = "    </div>\`;"
new_showcard_end = "    </div>\`;\n  addCardClick();"
content = content.replace(old_showcard_end, new_showcard_end, 1)

with open(path, 'w') as f:
    f.write(content)
print('✅ Card click fixed')
