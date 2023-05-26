import httpx
import asyncio
from bs4 import BeautifulSoup
import json
from random import randint
import logging
import aiofiles


async def pars(url: str = 'google.com', index: int = 0):
    await asyncio.sleep(randint(1, 5))
    page_data = []
    async with httpx.AsyncClient() as session:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'
        }
        response = await session.get(url=url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.read(), 'lxml')
            grid = soup.find(class_="market_content_block market_home_listing_table market_home_main_listing_table market_listing_table market_listing_table_active")
            items = grid.find_all('a', class_="market_listing_row_link")
            
            for item in items:
                
                page_data.append(
                    {
                        "href": item.get('href'),
                        "icon": item.find(class_="market_listing_item_img").get('src'),
                        "name": item.find(class_="market_listing_item_name").text,
                        "count": item.find(class_="market_listing_num_listings_qty").get('data-qty'),
                        'price': (item.find(class_="sale_price").text)#.replace('\r', '').replace('\n', '').replace('\t', '')
                    }
                )
        else:
            logging.error("Too much responces! Wait")
    #print(page_data)
    async with aiofiles.open(f'data/page_{index}.json', 'w', encoding='utf-8') as file:
        await file.write(f'{json.dumps(page_data, ensure_ascii=False, indent=2)}')
        print(f'Data saved to data/page_{index}')
async def main():
    pages_count=int(input('Count of pages:\n'))
    tasks = []

    for i in range(1, pages_count+1):
        tasks.append(pars(f'https://steamcommunity.com/market/search?appid=730#p{i}_popular_desc', index=i))

    await asyncio.gather(*tasks)
    


if __name__=='__main__':
    print('Counter-Strike: Global Offensive')
    asyncio.run(main())
