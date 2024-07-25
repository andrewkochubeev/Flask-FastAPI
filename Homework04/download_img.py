import argparse
import requests
import threading
import time
import asyncio
import aiohttp
from multiprocessing import Process

default_urls = [
    'https://ic.pics.livejournal.com/shakko.ru/2710882/4579528/4579528_800.jpg',
    'https://ic.pics.livejournal.com/shakko.ru/2710882/4580293/4580293_800.jpg',
    'https://ic.pics.livejournal.com/shakko.ru/2710882/4579262/4579262_original.jpg',
    'https://5koleso.ru/wp-content/uploads/2024/07/12revolution.jpg',
    'https://5koleso.ru/wp-content/uploads/2024/07/04revolution.jpg'
]


def download(url, path):
    start_time = time.time()
    response = requests.get(url)
    filename = path + url.split('/')[-1]
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


async def download_async(url):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            filename = 'async/' + url.split('/')[-1]
            with open(filename, "wb") as f:
                f.write(content)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


def threading_download(urls):
    threads = []
    print('\tЗагрузка изображений многопоточным методом')
    for url in urls:
        thread = threading.Thread(target=download, args=[url, 'thread/'])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def multiproc_download(urls):
    processes = []
    print('\tЗагрузка изображений многопроцессным методом')
    for url in urls:
        process = Process(target=download, args=(url, 'multiproc/',))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


async def main(urls):
    tasks = []
    print('\tЗагрузка изображений асинхронным методом')
    for url in urls:
        task = asyncio.ensure_future(download_async(url))
    tasks.append(task)
    await asyncio.gather(*tasks)


def download_case(method, urls):
    start_time = time.time()
    match method:
        case 'threading':
            threading_download(urls)
        case 'multiproc':
            multiproc_download(urls)
        case 'async':
            asyncio.run(main(urls))
        case 'all':
            threading_download(urls)
            multiproc_download(urls)
            asyncio.run(main(urls))
    print(f"\tОбщее затраченное время {time.time() - start_time:.2f} seconds")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download images with different methods(threading, multiprocessing, asynchronous)')
    parser.add_argument('-m', '--method', help='Download method: threading, multiproc, async or all(default)',
                        default='all',
                        choices=['threading', 'multiproc', 'async', 'all'])
    parser.add_argument('urls', nargs='*', help='Url of images that will be downloaded', default=default_urls)
    args = parser.parse_args()
    download_case(args.method, args.urls)
