from functions import *
from vk_api.longpoll import VkEventType
from alchemy_select import *
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

for event in send_bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = str(event.user_id)
        keyboard = VkKeyboard()
        keyboard.add_button('Начать поиск', VkKeyboardColor.PRIMARY)
        send_bot.send_but(event.user_id, f'Здравствуйте, {user_data.get_name(event.user_id)}, для поиска нажмите: Начать поиск', keyboard)
        for event in send_bot.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == "Начать поиск":
                    users_vk_id = user_data.search_user(user_id)
                    create_tables()
                    for profile_id in users_vk_id:
                        if (user_id, profile_id) not in select_of_table():
                            user_vk_link = 'vk.com/id' + str(profile_id)
                            user_photos = user_data.get_photo(profile_id, user_id)
                            send_bot.send_msg(user_id, user_vk_link)
                            add_in_table(user_id, profile_id)
                            try:
                                for i in user_photos:
                                    send_bot.send_photo(user_id, profile_id, i[0])
                                keyboard = VkKeyboard()
                                keyboard.add_button('Далее', VkKeyboardColor.POSITIVE)
                                send_bot.send_but(event.user_id,
                                             f'Чтобы получить новую анкету, нажмите: Далее',
                                             keyboard)
                            except Exception:
                                break
                            for event in send_bot.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    request = event.text
                                    if request == 'Далее':
                                        break
                        else:
                            continue
