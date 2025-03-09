import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup


async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=f"https://gmgn.ai/sol/token/J7TAvtou_znv3FZt2HFAvzYf5LxzVyryh3mBXWuTRRng25gEZAjh?nocache={random.randint(1, 100000)}",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
                "User-Agent": "Mozilla/5.0"
            }
        )
        
        html = result.html
        soup = BeautifulSoup(html, 'html.parser')

        script_tag = soup.find("script", id="__NEXT_DATA__")
        if not script_tag:
            print("Could not find token information in the page.")
            return

        data = json.loads(script_tag.string)
        token_info = data.get("props", {}).get("pageProps", {}).get("tokenInfo", {})
        holders = token_info.get("holder_count")
        top_10_rate = token_info.get("top_10_holder_rate")
        top_10_percentage = float(top_10_rate) * 100 if top_10_rate else None
        risk_info = {}
        risk_divs = soup.find_all("div", class_="css-1qbjn45")
        for div in risk_divs:
            label_tag = div.find("p", class_="chakra-text css-1rsuid4")
            if label_tag:
                label = label_tag.get_text(strip=True)
                if label in ["NoMint", "Blacklist"]:
                    value_div = div.find("div", class_="css-171onha")
                    if value_div:
                        # Assume the first <p> inside contains the risk value
                        value_tag = value_div.find("p")
                        if value_tag:
                            risk_value = value_tag.get_text(strip=True)
                            risk_info[label] = risk_value
        print("Number of Holders:", holders)
        if top_10_percentage is not None:
            print("Top 10 Holder Rate: {:.2f}%".format(top_10_percentage))
        else:
            print("Top 10 Holder Rate: Not available")

        print("Risk Info:")
        for key in ["NoMint", "Blacklist"]:
            print(f"  {key}: {risk_info.get(key, 'Not available')}")


if __name__ == "__main__":
    asyncio.run(main())
