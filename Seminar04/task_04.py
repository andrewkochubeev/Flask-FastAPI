import threading
import os

count = 0


def count_words(filename):
    global count
    with open(filename, encoding='utf-8') as f:
        text = f.read()
    count += len(text.split())
    print(f'Промежуточное значение {count = }')


threads = []

for root, dirs, files in os.walk('pages'):
    for file in files:
        file_path = os.path.join(root, file)
        thread = threading.Thread(target=count_words, args=[file_path])
        threads.append(thread)
        thread.start()

for thread in threads:
    thread.join()

print(f'Финальное значение {count = }')
