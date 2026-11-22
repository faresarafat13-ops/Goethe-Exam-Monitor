
import asyncio
from playwright.async_api import async_playwright

URL = "https://www.goethe.de/ins/jo/ar/spr/prf/gzb1.cfm"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(locale="ar-JO")

        try:
            response = await page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            await page.wait_for_timeout(5000)

            print("HTTP STATUS:",
                  response.status if response else "NO RESPONSE")

            print("PAGE TITLE:", await page.title())

            rows = page.locator("tr").filter(
                has=page.locator("button")
            )

            count = await rows.count()
            print("ROWS FOUND:", count)

            booked = await page.locator(
                "tr.nicht-buchbar"
            ).count()

            print("BOOKED ROWS:", booked)

            print("PAGE URL:", page.url)

            if count > 0:
                print("FIRST ROW:",
                      (await rows.first.inner_text())[:300])

        except Exception as e:
            print("TEST ERROR:", str(e))

        finally:
            await browser.close()

asyncio.run(main())
