from instagrapi import Client
from pathlib import Path
import sys


# put your image path here
image_path = 'img.jpeg'


def login_usr(username, password):
    cl = Client()
    cl.login(username, password)
    user_id = cl.user_id_from_username(username)

    print('just logged in!')
    return cl, user_id


def get_followings(cl, user_id):
    my_user_following = cl.user_following(user_id)

    print(f'got your following accounts: {len(my_user_following)} accounts')
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


def exclude_ids(cl, following_dict):
    with open('exclude.txt', 'r', encoding='utf-8') as ex_ids:
        ex_ids_list = ex_ids.read().splitlines()
        ex_ids.close()

    for user_id in ex_ids_list:
        print(f'removing {user_id} from the list...')
        user_id = cl.user_id_from_username(user_id)
        try:
            del following_dict[user_id]
        except:
            pass

    print(f'sending your message to {len(following_dict)} people after excluding some...')
    return following_dict


def get_following_log(following_dict):
    with open('following_log.txt', 'w') as f:
        user_followings_list = list(following_dict.keys())
        f.writelines('\n'.join(user_followings_list))

    print('done logged all following ids in following_log.txt')


def main(username, password):
    cl, my_user_id = login_usr(username, password)

    txt = get_msg()

    following_dict = get_followings(cl, my_user_id)
    get_following_log(following_dict)

    following_dict = exclude_ids(cl, following_dict)

    for user_id in following_dict:
        usershort_dict = following_dict[user_id].dict()
        u_name = usershort_dict['username']
        full_name = usershort_dict['full_name']

        out_txt = txt.replace("<u_name>", u_name)
        out_txt = out_txt.replace("<full_name>", full_name)

        cl.direct_send_photo(Path(image_path), [user_id])
        cl.direct_send(out_txt, [user_id])

        print(f'successful: sent to {u_name}')


if __name__ == '__main__':
    try:
        user_name = sys.argv[1]
        pass_word = sys.argv[2]
        main(user_name, pass_word)

    except Exception as e:
        print('usage: python3 main.py <username> <password>')
        print(e)
