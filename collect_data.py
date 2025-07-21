import pandas as pd
import requests


def fetch_data():
    # ID рангов: 4-Мифический, 5-Мифическая честь, 6-Мифическая слава
    RANK_IDS = [4, 5, 6]

    # Временные отрезки: 4-(месяц), 3-(7 дней), 2-(3 дня), 1-(1 день)
    TIME_FRAME = 3

    # Генерация ссылок
    urls = [f"https://mlbb.io/api/hero/filtered-statistics?rankId={id}&timeframeId={TIME_FRAME}" for id in RANK_IDS]

    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

    # Получение данных из запросов по ссылкам
    responses_list = [requests.get(url, headers=HEADERS).json()['data']for url in urls]

    return responses_list



def merge_fetch_data(responses_list):
    responses_dfs = [pd.DataFrame(response) for response in responses_list]
    combined_df = pd.concat(responses_dfs, ignore_index=True)

    result_df = combined_df.groupby('hero_name', as_index=False).agg({
        'win_rate': 'mean',
        'pick_rate': 'mean',
        'ban_rate': 'mean',
        'lane': 'first',
        'img_src': 'first'
    })

    return result_df




def recalculate_pick_rate(df):
    # Перерасчитываем pick_rate, чтобы он являлся предсказанием pick_rate, если бы героя не банили
    df['predicted_pick_rate'] = df['pick_rate'] + (df['ban_rate'] * df['pick_rate'] / 100)
    return df


def correct_hero_lanes(df):
    df.loc[df['hero_name'] == 'Popol and Kupa', 'lane'] = ['Jungle']
    return df


def translate_names(df):
    NAMES_MAP = pd.read_csv('names_map.csv').set_index('en_name')['ru_name']
    df['hero_name'] = df['hero_name'].map(NAMES_MAP).fillna(df['hero_name'])
    return df


def get_lane_top_heroes(df, lane):
    # Оставляем только персонажей нужной линии
    df = df[df['lane'].apply(lambda lane_list: lane in lane_list)]

    # Убираем персонажей которых редко выбирают
    quantile = df['pick_rate'].quantile(0.4)
    df = df[df['pick_rate'] > quantile]

    # Находим 5 сильнейших героев линии
    top_heroes = df.sort_values(by=['win_rate', 'pick_rate'], ascending=False)[:5]

    return top_heroes

def formate_win_rate(df):
    """
    Форматируем значения винрейтов, округляяя и превращая в строки со знаком процента
    Пример: 55.3321 --> 55%
    """
    df['win_rate'] = df['win_rate'].map('{:.0f}%'.format)
    return df


def get_top_heroes(df):
    LANES = ['Exp Lane', 'Gold Lane', 'Jungle', 'Mid Lane', 'Roam']
    for lane in LANES:
        top_heroes = get_lane_top_heroes(df, lane)
        top_heroes = formate_win_rate(top_heroes)
        top_heroes.to_csv('data/' + lane + '.csv', index=False)

        # Вывод информации о лучших героях на роль
        top_heroes.reset_index(drop=True, inplace=True)
        print(f'Определены самые сильные герои линии \033[1m {lane} \033[0m \n')
        print(top_heroes.drop(columns=['img_src', 'lane', 'predicted_pick_rate']))
        print('\n\n')


def get_top_heroes_for_ban(df):
    # Подсчитываем уровень угрозы персонажа на основе его процента побед и частоты выбора
    df['score'] = df['predicted_pick_rate'] * (df['win_rate'] - 50)

    ban_top = df.sort_values(by='score', ascending=False)[:12]
    ban_top.to_csv('data/ban_top.csv', index=False)

    # Вывод информации о лучших героях для запретов
    print(f'\033[1mОпределены самые лучшие герои для бана \033[0m \n')
    new_column_order = ["hero_name", "win_rate","score", "predicted_pick_rate", "pick_rate", "ban_rate"]
    ban_top = ban_top[new_column_order]
    ban_top.reset_index(drop=True, inplace=True)
    print(ban_top)


def collect_data():
    responses_list = fetch_data()
    df = (
        merge_fetch_data(responses_list)
            .pipe(recalculate_pick_rate)
            .pipe(correct_hero_lanes)
            .pipe(translate_names)
        )

    get_top_heroes(df)
    get_top_heroes_for_ban(df)



if __name__ == "__main__":
    collect_data()
