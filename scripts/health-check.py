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
        "https://winter-limit-2863.ploomber.app/health",
        "https://ai-career-assistant.cofun.digital/health",
        "https://socket-io-3i32.onrender.com/health"
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for url in urls:
            user_agent = random.choice(user_agents)

            context = await browser.new_context(
                user_agent=user_agent,
                viewport={"width": 1366, "height": 768},
                java_script_enabled=True,
                geolocation={"latitude": 37.7749, "longitude": -122.4194},
                permissions=["geolocation"],
            )

            page = await context.new_page()

            try:
                print(f"Checking {url} with User-Agent: {user_agent}")

                await asyncio.sleep(random.uniform(1, 3))  # Simulate human browsing delay

                response = await page.goto(url, wait_until="domcontentloaded")

                if response.status == 200:
                    print(f"{url} is up!")
                else:
                    print(f"{url} returned status {response.status}")
                    exit(1)

            except Exception as e:
                print(f"Error checking {url}: {e}")
                exit(1)

            finally:
                await context.close()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_health())
