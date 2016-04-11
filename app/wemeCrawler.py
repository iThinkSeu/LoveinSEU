import asyncio
import aiohttp

async def fetch_avatar(session, url):
	async with session.get(url) as response:
		if response.status == 200:
			img = await response.read()
			with open("avatar.jpg", "wb") as f:
				f.write(img)


loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
	loop.run_until_complete(fetch_avatar(session,'http://www.weme.space/avatar/37'))