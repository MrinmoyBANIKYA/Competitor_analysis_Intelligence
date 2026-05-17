import asyncio
from playwright.async_api import async_playwright
import time
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        
        print("Navigating to http://127.0.0.1:8501...")
        await page.goto("http://127.0.0.1:8501", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Fill credentials
        print("Entering email...")
        email_inputs = await page.query_selector_all('input[type="text"]')
        if len(email_inputs) > 0:
            await email_inputs[0].fill("admin@nixtio.com")
            
        print("Entering password...")
        pw_inputs = await page.query_selector_all('input[type="password"]')
        if len(pw_inputs) > 0:
            await pw_inputs[0].fill("nixtio_secure_2024")
            
        # Click Access Dashboard submit button
        print("Submitting login form...")
        btn = await page.query_selector('button:has-text("Access Dashboard")')
        if btn:
            await btn.click()
        else:
            # Try form submit or another selector
            await page.keyboard.press("Enter")
            
        await page.wait_for_timeout(5000)
        
        # Check if onboarding screen is present
        print("Checking onboarding...")
        onboard_btn = await page.query_selector('button:has-text("Start Setup")')
        if onboard_btn:
            await onboard_btn.click()
            await page.wait_for_timeout(2000)
            
        # Select "Quantitative Momentum" in the sidebar radio button
        print("Navigating to Quantitative Momentum...")
        # Streamlit radio labels are standard paragraphs or span texts
        radio_options = await page.query_selector_all('[data-testid="stSidebar"] [role="radiogroup"] label')
        for opt in radio_options:
            text = await opt.inner_text()
            if "Quantitative Momentum" in text:
                await opt.click()
                print("Clicked Quantitative Momentum menu item!")
                break
                
        await page.wait_for_timeout(5000)
        
        # Take a stunning screenshot to verify the layout
        screenshot_path = r"c:\Users\mrinm\OneDrive\Desktop\comp intelligence\sector-intelligence-tracker\screen.png"
        print(f"Taking screenshot and saving to {screenshot_path}...")
        await page.screenshot(path=screenshot_path)
        
        await browser.close()
        print("Verification complete successfully!")

if __name__ == "__main__":
    asyncio.run(main())
