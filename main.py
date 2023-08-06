from instagrapi import Client
from pathlib import Path
import argparse


# put your image path here
image_path = 'img.jpeg'


def login_usr(username, password):
    cl = Client()
    print('logging in...')
    cl.login(username, password)
    user_id = cl.user_id_from_username(username)

    print('just logged in!')
    return cl, user_id


def get_followings(cl, user_id):
    my_user_following = cl.user_following(user_id)

    print(f'got your following accounts: {len(my_user_following)} accounts')
    return my_user_following


def send(cl, img_path, text, user_id, u_name):
    try:
        cl.direct_send_photo(img_path, user_id)
        cl.direct_send(text, user_id)
        print(f'successful: sent to {u_name}')
    except:
        print(f"failed: couldn't sent to {u_name}")
        with open('failed_users.txt', 'a') as f:
            f.writelines(user_id)

def get_msg():
    with open('message.txt', 'r', encoding='utf-8') as msg:
        txt = msg.read()
        msg.close()

    print('got your message!')
    return txt


def exclude_ids(ids_file, cl,  following_dict):
    with open(ids_file, 'r', encoding='utf-8') as ex_ids:
        ex_ids_list = ex_ids.read().splitlines()

    for user_id in ex_ids_list:
        print(f'removing {user_id} from the list...')
        if args.exclude_ig_ids:
            user_id = cl.user_id_from_username(user_id)
        try:
            del following_dict[user_id]
        except:
            pass

    print(f'sending your message to {len(following_dict)} people after excluding some...')
    return following_dict


def include_ids(ids_file, cl,  following_dict):
    with open(ids_file, 'r', encoding='utf-8') as in_ids:
        in_ids_list = in_ids.read().splitlines()

        for user_id in in_ids_list:
            try:
                print(f'adding {user_id} to the list...')
                if args.include_ig_ids:
                    user_info = cl.user_info_by_username(user_id).dict()
                else:
                    user_info = cl.user_info(user_id).dict()
                
                following_dict[user_info['pk']] = user_info
                if args.follow_includes:
                    cl.user_follow(int(user_info['pk']))
                    print(f"just followed {user_id}.")
            except:
                print(f"failed to add {user_id} to the list.")

        print(f'sending your message to {len(following_dict)} people after including some...')
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

    if args.include_ids:
        following_dict = include_ids(args.include_ids, cl, following_dict)
    
    elif args.include_ig_ids:
        following_dict = include_ids(args.include_ig_ids, cl, following_dict)

    if args.exclude_ids:
        following_dict = exclude_ids(args.exclude_ids, cl, following_dict)
    
    elif args.exclude_ig_ids:
        following_dict = exclude_ids(args.exclude_ig_ids, cl, following_dict)


    for user_id in following_dict:
        if type(following_dict[user_id]) == type({}):
            usershort_dict = following_dict[user_id]
        else:
            usershort_dict = following_dict[user_id].dict()
        u_name = usershort_dict['username']
        full_name = usershort_dict['full_name']

        out_txt = txt.replace("<u_name>", u_name)
        out_txt = out_txt.replace("<full_name>", full_name)

        send(cl, Path(image_path), out_txt, [user_id], u_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='takes your account following users and shoots your ads in their DMs')
    parser.add_argument('-u', '--username', help='your account username to login.', required=True)
    parser.add_argument('-p', '--password', help='your account password to login.', required=True)

    parser.add_argument('-F', '--follow_includes', action='store_true',
                        help='follows the included list before sending the message to them. '
                             'only works when the include list(-i or -I) is available.')

    parser.add_argument('-i', '--include_ids', help='includes accounts using a given file of the API ids.')
    parser.add_argument('-I', '--include_ig_ids',
                        help='includes accounts using a given file of the normal instagram ids.')
    parser.add_argument('-e', '--exclude_ids', help='excludes accounts using a given file of the API ids.')
    parser.add_argument('-E', '--exclude_ig_ids',
                        help='excludes accounts using a given file of the normal instagram ids.')
    args = parser.parse_args()

    main(args.username, args.password)
