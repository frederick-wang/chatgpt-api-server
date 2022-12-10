from playwright.sync_api import sync_playwright
from config import context, cookie_vars

START_URL = "https://chat.openai.com/chat"
PLAYWRIGHT = sync_playwright().start()
CONTEXT = PLAYWRIGHT.chromium.launch_persistent_context(
    user_data_dir="USER_DATA_DIR",
    headless=True,
    user_agent=context['user_agent'],
)
content_cookies_names = {
    c['name'] for c in CONTEXT.cookies(START_URL) if 'name' in c
}
for c in cookie_vars:
    if 'name' in c and c['name'] not in content_cookies_names:
        CONTEXT.add_cookies([c])
# Set Key 'oai/apps/hasSeenOnboarding/chat' to 'true'
CONTEXT.add_init_script("localStorage.setItem('oai/apps/hasSeenOnboarding/chat', 'true');")
