import requests
import re
import os

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 ' \
             'Safari/537.36 '


def get_picture(post):
    r = requests.get(f'https://{id}.lofter.com/post/{post}', headers={'User-Agent': user_agent})
    pics = re.findall('(?<=bigimgsrc=").*?(?=\\?)', r.text)
    print(pics)
    cnt = 0
    for pic in pics:
        extension = pic[-3:]
        print(f'{id}/{post}_{cnt}.{extension}')
        cnt = cnt + 1
        with open(f'{id}/{post}_{cnt}.{extension}', 'wb') as f:
            f.write(requests.get(pic, headers={'User-Agent': user_agent}).content)


def proc():
    page = 1
    while True:
        r = requests.get(f'https://{id}.lofter.com/?page={page}', headers={'User-Agent': user_agent})
        # print(r.text)
        posts = re.findall('(?<=/post/).*?(?=">)', r.text)
        unique_posts = list(set(posts))
        print(unique_posts)
        for post in unique_posts:
            get_picture(post)
        if len(posts) == 0 or page > 1000:
            break
        page += 1


if __name__ == '__main__':
    print("输入Lofter id（指url上的id）：")
    id = input()
    if not os.path.exists(id):
        os.mkdir(id)
    proc()
