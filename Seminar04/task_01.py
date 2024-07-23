import requests
import threading
import time

urls = [
    'https://vk.com/',
    'https://youtube.com',
    'https://wireframe.cc/WJ4Lb1',
    'https://letsencrypt.org/ru/',
    'https://getbootstrap.com/docs/5.3/components/button-group/',
    'https://edit.org/edit/all/14sxb7zt9',
    'https://pythontutor.com/render.html#mode=edit',
    'https://timeweb.cloud',
    'https://linkmeup.ru/blog/',
    'https://ya.ru'
]


def download(url):
    response = requests.get(url)
    filename = 'pages/threading_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    with open(filename, "w", encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


threads = []
start_time = time.time()

for url in urls:
    thread = threading.Thread(target=download, args=[url])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
