import vk_api
import config
import time

vk_session = vk_api.VkApi(config.phone, config.pas)


# для двухфакторной аутентификации
def auth_handler():
    key = input('Enter code: ')
    remember_device = True

    return key, remember_device


def main():
    login, password = config.phone, config.pas
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)
    photos = tools.get_all('photos.get', 50, {
        "owner_id": config.owner_id,
        'album_id': 'saved',
        'rev': 1,
        'count': 100})

    vk = vk_session.get_api()
    array = []
    for i in range(100):  # позже - переписать итерацию, рендж заменить на кол-во фоток, сделав соответствующий запрос
        photo_id = photos['items'][i]['id']
        array.append(photo_id)

    item = 1
    for idx in array:
        item += 1
        time.sleep(2)
        print(vk.likes.add(owner_id=config.owner_id, item_id=idx, type='photo'), '№-',
              item)  # позже - предоставить выбор типа объекта, идентификатор пользователя и т.д.


if __name__ == '__main__':
    main()
