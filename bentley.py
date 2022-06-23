import asyncio
from typing import List

import aiohttp


async def signup_bentley(email: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://nft.bentleymotors.com/api/signup",
            json={"email": email}
        ) as resp:
            return resp.status


async def main(emails: list) -> List[int]:
    tasks = [asyncio.create_task(signup_bentley(email)) for email in emails]

    return await asyncio.gather(*tasks)
