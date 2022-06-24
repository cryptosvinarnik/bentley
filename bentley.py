import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

import aiohttp
from fake_useragent import UserAgent as ua
from twocaptcha import TwoCaptcha


solver = TwoCaptcha(input("TwoCaptcha api key:"))


def solve_captcha():
    return solver.recaptcha(
        sitekey='6LfK9JYgAAAAALK-wl-2YwNySarhvFLyErhOsOjB',
        url='https://nft.bentleymotors.com/',
    )


async def signup_bentley(email: str) -> int:
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as pool:
        resp = await loop.run_in_executor(
            pool,
            lambda: solve_captcha()
        )

    headers = {
        "Host": "nft.bentleymotors.com",
        "User-Agent": ua().random,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://nft.bentleymotors.com/",
        "Content-Type": "application/json",
        "Origin": "https://nft.bentleymotors.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
            "https://nft.bentleymotors.com/api/signup",
            json={"email": email, "token": resp['code']}
        ) as resp:
            return resp.status


async def main(emails: list) -> List[int]:
    tasks = [asyncio.create_task(signup_bentley(email)) for email in emails]

    return await asyncio.gather(*tasks)
