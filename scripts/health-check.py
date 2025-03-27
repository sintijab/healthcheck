import asyncio
import random
from playwright.async_api import async_playwright

async def check_health():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.119 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
    ]

    urls = [
        "https://jolly-grass-4575.ploomber.app/health",
        "https://ai-career-assistant.cofun.digital/health",
        "https://sound-master-chat.onrender.com/health"
    ]

    max_retries = 3
    retry_delay = 10

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=60000)

        for url in urls:
            user_agent = random.choice(user_agents)

            context = await browser.new_context(
                user_agent=user_agent,
                viewport={"width": 1366, "height": 768},
                java_script_enabled=True,
                geolocation={"latitude": 37.7749, "longitude": -122.4194},
                permissions=["geolocation"],
            )
            context.set_default_timeout(60000)
            page = await context.new_page()

            retries = 0
            while retries <= max_retries:
                try:
                    print(f"Checking {url} (Attempt {retries + 1}) with User-Agent: {user_agent}")

                    await asyncio.sleep(random.uniform(1, 40))
                    page.set_default_timeout(60000)

                    response = await page.goto(url, wait_until="domcontentloaded", timeout=60000)

                    if response.status == 200:
                        print(f"{url} is up!")
                        break
                    else:
                        print(f"{url} returned status {response.status}, retrying...")
                        retries += 1
                        await asyncio.sleep(retry_delay * (2 ** retries))

                except Exception as e:
                    print(f"Error checking {url}: {e}, retrying...")
                    retries += 1
                    await asyncio.sleep(retry_delay * (2 ** retries))

                if retries > max_retries:
                    print(f"Failed to check {url} after {max_retries} retries.")
                    exit(1)

            await context.close()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_health())
