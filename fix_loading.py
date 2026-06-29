path = '/data/data/com.termux/files/home/amore-web/index.html'
with open(path, 'r') as f:
    content = f.read()

# Add loading page
old_login_page = "<!-- LOGIN PAGE -->"
new_login_page = """<!-- LOADING PAGE -->
<div class="page active" id="loadingPage" style="align-items:center;justify-content:center;background:linear-gradient(135deg,#FF4B6E,#FF8C6B)">
  <div style="text-align:center;color:#fff">
    <div style="font-size:72px">💕</div>
    <div style="font-size:32px;font-weight:800;margin-top:8px">Amore</div>
    <div style="margin-top:24px"><div class="spinner" style="border-color:rgba(255,255,255,0.3);border-top-color:#fff;margin:0 auto"></div></div>
  </div>
</div>

<!-- LOGIN PAGE -->"""

content = content.replace(old_login_page, new_login_page)

# Show loading first, then switch based on auth state
old_auth = """onAuthStateChanged(auth, async (user) => {
  if (user) {"""

new_auth = """onAuthStateChanged(auth, async (user) => {
  if (user) {
    showPage('loadingPage');"""

content = content.replace(old_auth, new_auth)

with open(path, 'w') as f:
    f.write(content)
print('✅ Loading screen added')
