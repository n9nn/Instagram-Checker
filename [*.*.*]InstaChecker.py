import asyncio
import random
import string
import time
import os
import aiohttp
from blood import InstagramTurbo
SESSION_ID = "YOUR_INSTAGRAM_SESSION_ID_HERE"
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

PROXIES = [
    # "http://user:pass@ip:port",
]
MAX_REQ_PER_SEC = 28
BATCH_SIZE = 25

stats = {
    "requests": 0,
    "success": 0,
    "blocks_429": 0,
    "errors": 0,
    "last_checked": "None"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def send_telegram(session: aiohttp.ClientSession, msg: str):
    if TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        async with session.post(url, json=payload, timeout=5) as response:
            await response.text()
    except Exception:
        pass

def generate_custom_patterns(count=25):
    letters = string.ascii_lowercase
    digits = string.digits
    patterns = []
    choices_types = [
        ("letter", "digit", "letter"),
        ("digit", "letter", "letter"),
        ("letter", "letter", "digit")
    ]
    for _ in range(count):
        pattern_type = random.choice(choices_types)
        parts = [random.choice(letters if item == "letter" else digits) for item in pattern_type]
        patterns.append(".".join(parts))
    return patterns

def print_dashboard(start_time: float, current_user: str):
    clear_screen()
    elapsed = time.time() - start_time
    rps = stats["requests"] / elapsed if elapsed > 0 else 0
    rpm = rps * 60

    print("=" * 60)
    print("    🔥 BLOOD TURBO IQ - PATTERN SNIPER + PROXIES 🔥")
    print("=" * 60)
    print(f" [*] Last Checked    : @{current_user}")
    print(f" [*] Elapsed Time    : {int(elapsed)} seconds")
    print("-" * 60)
    print(f" 📊 Total Requests   : {stats['requests']}")
    print(f" ⚡ Speed (RPS)      : {rps:.2f} req/sec")
    print(f" 🚀 Speed (RPM)      : {rpm:.1f} req/min")
    print("-" * 60)
    print(f" ⚠️  Rate Limits (429): {stats['blocks_429']}")
    print(f" ❌ Errors / Other   : {stats['errors']}")
    print("=" * 60)
    print(" [!] Sniping active... Press Ctrl+C to stop.")

async def worker(turbo, session, username, start_time):
    stats["requests"] += 1
    stats["last_checked"] = username
    
    result = await turbo.safe_async_claim(session, username)
    status = result.get("status_code", 0)
    
    if result.get("success"):
        stats["success"] += 1
        print(f"\n[+] SUCCESS! Target Claimed: @{username}")
        
        alert_msg = (
            f"🔥 **[BLOOD TURBO - PATTERN SNIPED!]** 🔥\n\n"
            f"👤 **Username:** `@{username}`\n"
            f"📊 **Total Scans:** `{stats['requests']}`\n"
            f"⏱️ **Time Elapsed:** `{int(time.time() - start_time)}s`\n"
            f"🌐 **Proxy Mode:** `Rotating Residential`"
        )
        await send_telegram(session, alert_msg)
        return True
        
    elif status == 429:
        stats["blocks_429"] += 1
        await asyncio.sleep(0.5)
    else:
        stats["errors"] += 1
        
    print_dashboard(start_time, username)
    return False

async def main():
    turbo = InstagramTurbo(
        session_id=SESSION_ID,
        proxies=PROXIES,
        max_requests_per_sec=MAX_REQ_PER_SEC
    )

    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        await send_telegram(session, "🚀 **[BLOOD PATTERN SNIPER STARTED]**\nMode: `Residential Proxies + Random Patterns (*.*.*)`")
        
        while True:
            usernames = generate_custom_patterns(BATCH_SIZE)
            
            for uname in usernames:
                is_claimed = await worker(turbo, session, uname, start_time)
                if is_claimed:
                    print(f"\n[✨] Got hunt this @{uname} .")
                    return
                
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[!] Engine terminated by user.")
  
