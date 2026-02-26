import requests
from datetime import datetime


def convert_timestamp(timestamp):
    if timestamp:
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return "Не найдено"


def get_ban_status(bans_data):
    if not bans_data:
        return "Нет информации о банах"

    vac_status = "Есть VAC бан" if bans_data.get('vacBanned') else "Нет VAC бана"
    game_bans = bans_data.get('numberOfGameBans', 0)
    vac_bans = bans_data.get('numberOfVACBans', 0)

    result = f"{vac_status}"
    if vac_bans > 0:
        result += f" ({vac_bans} шт.)"
    if game_bans > 0:
        result += f", Game банов: {game_bans}"

    return result


def get_online_status(persona_state):
    statuses = {
        0: "Оффлайн",
        1: "Онлайн",
        2: "Занят",
        3: "Нет на месте",
        4: "Спит",
        5: "В торговле",
        6: "Ищет игру"
    }
    return statuses.get(persona_state, "Неизвестно")


def get_steam_data(steam_id):
    url = f'https://api.findsteamid.com/api/steamuser/{steam_id}'
    url_friends = f'https://api.findsteamid.com/api/steamuser/friends/{steam_id}'

    try:
        response1 = requests.get(url)
        response2 = requests.get(url_friends)

        profile_data = response1.json() if response1.status_code == 200 else None
        friends_data = response2.json() if response2.status_code == 200 else None

        return profile_data, friends_data

    except requests.exceptions.RequestException:
        print(f"Ошибка, пишите sh1ro")
        return None, None
    except Exception as e:
        print(f"Ошибка, пишите sh1ro")
        return None, None


def display_profile_info(profile_data):
    if not profile_data:
        print("Нет данных о профиле")
        return

    profile = profile_data[0]
    bans = profile.get('bans', {})

    print("=" * 70)
    print("ИНФОРМАЦИЯ О ПРОФИЛЕ STEAM")
    print("=" * 70)
    print(f"Steam ID:          {profile.get('steamId', 'Не найдено')}")
    print(f"Имя профиля:       {profile.get('personaName', 'Не найдено')}")
    print(f"Настоящее имя:     {profile.get('realName', 'Не найдено')}")
    print(f"Ссылка на профиль: {profile.get('profileUrl', 'Не найдено')}")
    print(f"Статус:            {get_online_status(profile.get('personaState', 0))}")
    print(f"Видимость профиля: {'Публичный' if profile.get('communityVisibilityState') == 3 else 'Приватный'}")
    print(f"Страна:            {profile.get('locCountryCode', 'Не найдено')}")
    print(f"Дата создания:     {convert_timestamp(profile.get('timeCreated'))}")
    print(f"Последний вход:    {convert_timestamp(profile.get('lastLogoff'))}")
    print(f"Статус банов:      {get_ban_status(bans)}")

    if bans.get('daysSinceLastBan', 0) > 0:
        print(f"Дней с бана:       {bans.get('daysSinceLastBan')}")

    print("-" * 70)


def display_friends_info(friends_data):
    if not friends_data:
        print("Нет данных о друзьях или профиль приватный")
        return

    print("\n" + "=" * 70)
    print(f"СПИСОК ДРУЗЕЙ ({len(friends_data)} человек)")
    print("=" * 70)

    sorted_friends = sorted(friends_data, key=lambda x: x.get('personaState', 0), reverse=True)

    online_count = 0
    vac_banned_count = 0
    game_banned_count = 0

    for i, friend in enumerate(sorted_friends, 1):
        bans = friend.get('bans', {})
        is_online = friend.get('personaState', 0) > 0
        has_vac = bans.get('vacBanned', False)
        has_game_ban = bans.get('numberOfGameBans', 0) > 0

        if is_online:
            online_count += 1
        if has_vac:
            vac_banned_count += 1
        if has_game_ban:
            game_banned_count += 1

        status_prefix = "[ONLINE] " if is_online else "[OFFLINE]"

        print(f"\n{i}. {status_prefix} {friend.get('personaName', 'Без имени')}")
        print(f"   Steam ID:        {friend.get('steamId')}")
        print(f"   Статус:          {get_online_status(friend.get('personaState', 0))}")

        if friend.get('realName'):
            print(f"   Настоящее имя:   {friend.get('realName')}")

        if friend.get('locCountryCode'):
            print(f"   Страна:          {friend.get('locCountryCode')}")

        if friend.get('gameExtraInfo'):
            print(f"   В игре:          {friend.get('gameExtraInfo')}")

        ban_info = []
        if has_vac:
            ban_info.append(f"VAC: {bans.get('numberOfVACBans', 0)}")
        if has_game_ban:
            ban_info.append(f"Game: {bans.get('numberOfGameBans', 0)}")

        if ban_info:
            print(f"   Баны:            {', '.join(ban_info)}")
        else:
            print(f"   Баны:            Нет")

        print(f"   Профиль:         {friend.get('profileUrl')}")
        print("   " + "-" * 50)

    print(f"\nСТАТИСТИКА ДРУЗЕЙ:")
    print(f"   Всего друзей:    {len(friends_data)}")
    print(f"   Онлайн:          {online_count}")
    print(f"   Оффлайн:         {len(friends_data) - online_count}")
    print(f"   С VAC банами:    {vac_banned_count}")
    print(f"   С Game банами:   {game_banned_count}")
    print(f"   Без VAC: {len(friends_data) - vac_banned_count - game_banned_count}")
