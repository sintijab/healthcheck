const { chromium } = require('playwright');

(async () => {
    const userAgents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.119 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
    ];

    const urls = [
        "https://winter-limit-2863.ploomber.app/health",
        "https://ai-career-assistant.cofun.digital/health",
        "https://socket-io-3i32.onrender.com/health"
    ];

    const browser = await chromium.launch({ headless: true });

    for (const url of urls) {
        const userAgent = userAgents[Math.floor(Math.random() * userAgents.length)];

        const context = await browser.newContext({
            userAgent,
            viewport: { width: 1366, height: 768 },
            javaScriptEnabled: true,
            storageState: undefined,
            geolocation: { latitude: 37.7749, longitude: -122.4194 },
            permissions: ['geolocation'],
        });

        const page = await context.newPage();

        try {
            console.log(`Checking ${url}`);

            await page.waitForTimeout(Math.random() * 2000 + 1000);

            const response = await page.goto(url, { waitUntil: "domcontentloaded" });

            if (response.status() === 200) {
                console.log(`${url} is up!`);
            } else {
                console.error(`${url} returned status ${response.status()}`);
                process.exit(1);
            }
        } catch (error) {
            console.error(`Error checking ${url}:`, error);
            process.exit(1);
        } finally {
            await context.close();
        }
    }

    await browser.close();
})();
