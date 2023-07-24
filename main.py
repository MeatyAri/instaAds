from instagrapi import Client
from pathlib import Path
import sys


# put your image path here
image_path = 'img.jpg'


def login_usr(username, password):
    cl = Client()
    cl.login(username, password)
    user_id = cl.user_id_from_username(username)

    print('just logged in!')
    return cl, user_id


def get_followings(cl, user_id):
    my_user_following = cl.user_following(user_id)

    print(f'sending your message to {len(my_user_following)} people...')
    return my_user_following


def send_text(cl, text, user_id):
    cl.direct_send(text, user_id)


def send_image(cl, img_path, user_id):
    cl.direct_send_photo(img_path, user_id)


def get_msg():
    with open('message.txt', 'r', encoding='utf-8') as msg:
        txt = msg.read()
        msg.close()

    print('got your message!')
    return txt


def main(username, password):
    cl, my_user_id = login_usr(username, password)

    txt = get_msg()

    following_dict = get_followings(cl, my_user_id)

    for user_id in following_dict:
        cl.direct_send_photo(Path(image_path), [user_id])
        cl.direct_send(txt, [user_id])

        usershort_dict = following_dict[user_id].dict()
        u_name = usershort_dict['username']
        print(f'successful: sent to {u_name}')


if __name__ == '__main__':
    try:
        user_name = sys.argv[1]
        pass_word = sys.argv[2]
        main(user_name, pass_word)

    except Exception as e:
        print('usage: python3 main.py <username> <password>')
        print(e)
