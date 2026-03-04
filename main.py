import asyncio
import re

import instaloader
import uvicorn

from utils.steamsearch import get_steam_data, display_profile_info, display_friends_info
from utils.shiromu_helper import shhelper_help
from utils import metasearch
import localdb.localdbsearch
import utils.phonenumber_search as pn
from utils.Telegram_connect import run_bot_flow
from utils.email_search import search_email_lullar_simple, print_results, search_email_lullar_advanced
from utils.imports import *
from utils import doxpastecreate
from utils.darklinks import *
from Config.func_comments_return import *
from utils.ip_osint import get_info_by_ip, get_ip_by_hostname
from utils import create_fake_paste
from utils import all_parsers
from allbanners import banner1, banner2, banner3, banner4
from smscallbomber import SMSCallBomber
from utils import nicks
from utils.discord_osint import get_discord_user_info, get_info_by_dsid, get_all_nicknames, get_nicks_by_id, \
    get_friends_by_id, sobitiya_usera, voice_history, format_voice_history
import sys
import subprocess
import sys
from pathlib import Path

os.system('cls' if os.name == 'nt' else 'clear')


class leave_from_tool:
    def __init__(self):
        pass

    def leave(self, vd):
        if vd == 0:
            print('Завершиние работы...')
            return True
        return False


def init():
    pass


init()

lf = leave_from_tool()

while True:
    try:

        banner1.banner_one()

        vd = int(input("Выберите действие: "))

        if lf.leave(vd):
            break

        if vd == 1:
            phone_number = input("Введите номер телефона(формат: +79304669445): ")
            res = pn.get_phone_number_info(phone_number)
            shhelper_help(results=res)
        if vd == 2:
            z = input('Введите информацию о таргете: ')
            try:
                localdb.localdbsearch.local_db_srch(z=z)
            except Exception as e:
                print(e)

        if vd == 3:
            print("Перед началом использования, пожалуйста, добавьте изображения в директорию imgs, спасибо")
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                directory = os.path.join(script_dir, "imgs")
                metasearch.process_images_in_directory(directory)
            except Exception as e:
                print(e)
        if vd == 4:
            z = input('Введите информацию о таргете: ')
            try:
                localdb.localdbsearch.local_db_srch(z=z)
            except Exception as e:
                print(e)

        if vd == 7:
            ip = input("Введите IP-адрес таргета: ")
            results = get_info_by_ip(ip=ip)
            if results:
                shhelper_help(results=results)
            else:
                print("Не удалось получить информацию по IP")

        if vd == 5:
            il = instaloader.Instaloader()
            name = input("Введите username таргета: ")


            def inst_osint(username):
                profile = instaloader.Profile.from_username(il.context, username=username)
                print(
                    f'Информация о профиле: {username}\n {profile.biography}\n Постов: {profile.mediacount}\nПодписчиков: {profile.followers}')


            print(inst_osint(username=name))

        if vd == 20:
            with open("aboutshiromu.txt", "r", encoding="utf-8") as file:
                content = file.read()
                print(content)

        if vd == 8:
            hostname = input("Введите домен: ")
            print(get_ip_by_hostname(hostname=hostname))

        if vd == 13:
            async def main():
                with open('sessions.txt', 'r') as f:
                    auth = f.read()
                    auth_api_id_nachalo = auth.find('api_id=') + len('api_id=')
                    auth_api_id_konez = auth.find('\n', auth_api_id_nachalo)
                    api_id_itog = auth[
                                  auth_api_id_nachalo:auth_api_id_konez].strip() if auth_api_id_nachalo != -1 else None
                    api_hash_nach = auth.find('api_hash=') + len('api_hash=')
                    api_hash_kon = auth.find('\n', api_hash_nach)
                    if api_hash_kon == -1:
                        api_hash_itog = auth[api_hash_nach:].strip()
                    else:
                        api_hash_itog = auth[api_hash_nach:api_hash_kon].strip()
                print(api_id_itog)
                print(api_hash_itog)
                hasssh = api_hash_itog
                iddd = api_id_itog
                msg_txt = input('Введите информацию о таргете: ')

                ress = await run_bot_flow(iddd, hasssh, msg_txt)
                print("\nИтоговые результаты:")
                for bot, messages in ress.items():
                    print(f"\n{bot}:")
                    if messages:
                        for msg in messages:
                            print(f"- {msg}")
                    else:
                        print("Нет результатов")


            if __name__ == "__main__":
                asyncio.run(main())

        if vd == 14:
            print(indev_soon)

        if vd == 9:
            def is_port_open(host, port):
                s = socket.socket()
                try:
                    s.connect((host, port))
                except:
                    return False
                else:
                    return True


            host = input("Введите IP таргета:")
            print("Сканирование запущено, ожидайте...")
            for port in range(1, 1025):
                if is_port_open(host, port):
                    print(f"[+] {host}:{port} открыт")
                else:
                    print(f"[!] {host}:{port} закрыт", end="\r")

        if vd == 26:
            create_fake_paste.generate_fake_paste()

        if vd == 52:
            try:
                asyncio.run(nicks.main())
            except KeyboardInterrupt:
                print("\nВыход в главное меню...")
        if vd == 6:
            print(indev_soon)

        if vd == 15:
            phone = int(input("Введите номер таргета(без+): "))
            args = Namespace(country='ALL', phone=phone, time=20, threads=4, timeout=10, proxy=False)
            args.time += time.time()

            attack_threads = {}
            bombers = {}
            bomber_id = 1234567890


            def attack_thread_runner(args):
                bomber = SMSCallBomber(args)
                bombers[bomber_id] = bomber
                bomber.run()


            attack_threads = threading.Thread(target=attack_thread_runner, args=(args,))
            attack_threads.start()

            attack_threads.join(0)
            del attack_threads
            time.sleep(10)
            bomber = bombers[bomber_id]
            bomber.stop()
            successful, failed = bomber.send_report()
            print(f"Сообщений отправлено: {successful}")
            print(f"Не удалось отправить: {failed}")

            time.sleep(10)
            bomber = bombers[bomber_id]
            successful, failed = bomber.send_report()
            print(f"Сообщений отправлено: {successful}")
            print(f"Не удалось отправить: {failed}")

        if vd == 21:

            print(Fore.RED + "[81] Стартовый мануал по ОСИНТУ")
            print(Fore.RED + "[82] Мануал по сносу тг")
            print(Fore.RED + "[83] Мануал по сносу тгк")

            vibor = int(input("Выберите мануал: "))

            if vibor == 81:
                with open("OSINT.txt", "r", encoding="utf-8") as file:
                    osint = file.read()
                    print(osint)
            if vibor == 82:
                with open("snostg.txt", 'r', encoding='utf-8') as file:
                    snostg = file.read()
                    print(snostg)
            if vibor == 83:
                with open('snostgc.txt', 'r', encoding='utf-8') as file:
                    snostgc = file.read()
                    print(snostgc)

        if vd == 27:
            API = 'https://www.1secmail.com/api/v1/'
            domains = ["1secmail.com", "1secmail.org", "1secmail.net", "wwjmp.com", "esiix.com", "xojxe.com",
                       "yoggm.com"]
            domain = random.choice(domains)


            def create_username():
                usrname = string.ascii_lowercase + string.digits
                username = ''.join(random.choice(usrname) for i in range(10))
                return username


            def check_mail(mail=''):
                req_link = f'{API}?action=getMessages&login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
                r = requests.get(req_link).json()
                leghth = len(r)

                if leghth == 0:
                    print('Пусто :(, обновляется каждые 5 сек')
                else:
                    id_list = []

                    for i in r:
                        for k, v in i.items():
                            if k == 'id':
                                id_list.append(v)
                    print(f'{leghth} сообщений. Обновляется каждые 5 сек')
                    current_dir = os.getcwd()
                    final_dir = os.path.join(current_dir, 'all_mails')
                    if not os.path.exists(final_dir):
                        os.makedirs(final_dir)

                    for i in id_list:
                        read_msg = f'{API}?action=readMessage&login={mail.split("@")[0]}&domain={mail.split("@")[1]}&id={i}'
                        r = requests.get(read_msg).json()

                        sender = r.get('from')
                        subject = r.get('subject')
                        date = r.get('date')
                        content = r.get('textBody')

                        mail_file_path = os.path.join(final_dir, f'{i}.txt')

                        with open(mail_file_path, 'w') as file:
                            file.write(
                                f'Отправитель: {sender}\nНа анон почту: {mail}\nФайлы: {subject}\nДата: {date}\nСодержимое:{content}')


            def main():
                try:
                    username = create_username()
                    mail = f'{username}@{domain}'
                    print(f'Временная анон почта: {mail}')

                    mail_req = requests.get(f'{API}?login={mail.split("@")[0]}&domain={mail.split("@")[1]}')

                    while True:
                        check_mail(mail=mail)
                        time.sleep(5)

                except(KeyboardInterrupt):
                    print("Прервано")


            if __name__ == '__main__':
                main()

        if vd == 19:
            banner2.banner_two()

        if vd == 31:
            while True:
                name_pasta = input('Введите информацию, которую вы уже знаете о таргете: ').replace(
                    '_', '')
                name_pasta = name_pasta.replace(' ', '')
                if name_pasta == '':
                    print('Некорректно введена информация... ')
                else:
                    all_parsers.doxbin_parser(f'https://doxbin.org/upload/{name_pasta}')

        if vd == 30:
            print_darklist(darklist)

        if vd == 32:
            doxpastecreate.main()

        if vd == 11:
            banner3.banner_three()

        if vd == 10:
            email = input("Введите email для поиска: ").strip()

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("❌ Введите корректный email адрес!")
            else:
                print(f"🔍 Ищем соцсети для: {email}")

                results = search_email_lullar_simple(email)
                print_results(results, email)

                if results:
                    shhelper_help(results=results)
                if not results:
                    print("Пробуем альтернативный метод поиска...")
                    results = search_email_lullar_advanced(email)
                    print_results(results, email)

        if vd == 35:
            banner4.banner_four()

        if vd == 38:
            username = input("Введите Discord username/ID таргета: ")
            result = get_discord_user_info(username)
            print(result)
            shhelper_help(results=result)

        if vd == 37:
            user_id = input("Введите Discord ID таргета: ").strip()

            if user_id:
                result = get_info_by_dsid(user_id)
            else:
                result = get_info_by_dsid(user_id)

            if result:
                print("\n📋 ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")
                print(f"Discord ID: {result['discord_id']}")
                print(f"Всего серверов: {result['total_servers']}")
                print(f"Текущих серверов: {len(result['current_servers'])}")
                print(f"Покинутых серверов: {len(result['left_servers'])}")

                if result['current_servers']:
                    print("\n🏠 ТЕКУЩИЕ СЕРВЕРА:")
                    for server in result['current_servers']:
                        print(f"  - {server['name']} (ID: {server['id']})")
            shhelper_help(results=result)

        if vd == 39:
            user_id = input("Введите Discord ID таргета: ").strip()

            result = get_nicks_by_id(user_id)

            if result:
                print("\n📋 ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")
                print(f"Discord ID: {result['discord_id']}")
                print(f"Всего никнеймов: {result['total_count']}")

                unique_servers = set()
                for nick in result['nicknames']:
                    if nick.get('guild'):
                        unique_servers.add(nick['guild']['name'])

                print(f"Уникальных серверов: {len(unique_servers)}")

                if result['has_next_page']:
                    print("\n🔄 Получение всех никнеймов...")
                    all_nicks = get_all_nicknames(user_id)
                    print(f"Все nicknames: {len(all_nicks)}")
            shhelper_help(results=result)

        if vd == 40:
            us_id = input('Введите discord ID таргета:')
            get_friends_by_id(user_id=us_id)

        if vd == 41:
            us_id = input('Введите discord ID таргета:')
            res = sobitiya_usera(user_id=us_id)

        if vd == 42:
            us_id = input('Введите discord ID таргета:')
            res = voice_history(user_id=us_id)
            url = f'https://discord-sensor.com/api/users/get-latest-events/{us_id}?subTab=voice_history&limit=20&page=1'
            response = requests.get(url)
            data = response.json()
            dlya_helpera = format_voice_history(data)
            shhelper_help(results=dlya_helpera)

        if vd == 43:
            def main():
                targ_id = input('Введите STEAM ID таргета: ')

                print("Получение данных...")
                profile_data, friends_data = get_steam_data(targ_id)

                if profile_data:
                    display_profile_info(profile_data)
                else:
                    print("Не удалось получить данные профиля")

                if friends_data:
                    display_friends_info(friends_data)
                else:
                    print("Не удалось получить информацию о кентах")


            if __name__ == "__main__":
                main()
        if vd == 44:
            GRAPHS_PATH = Path(__file__).parent / "Graphs"
            WEBAPP_PATH = GRAPHS_PATH / "webapp.py"


            def run_webapp():
                print("🚀 Запуск SHIROMU VISUALIZATION...")
                if not WEBAPP_PATH.exists():
                    print(f"Путь не найден")
                    return

                try:
                    subprocess.run([sys.executable, str(WEBAPP_PATH)])
                except KeyboardInterrupt:
                    print("\n Bye Bye")
                except Exception as e:
                    print(f" Error")


            if __name__ == "__main__":
                run_webapp()

        if vd in [91, 16, 17, 18, 78, 93, 33, 34, 22, 29, 52]:  # 22
            print(ifv)

    except Exception as e:
        print('Что-то не так, возвращаю в главное меню, пожалуйста, сообщите Sh1ro об ошибке...')
        continue
