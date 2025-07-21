from jinja2 import Environment, FileSystemLoader
import pandas as pd

DATA_CONFIG = [
    {
        'file_path': 'data/Gold Lane.csv',
        'title': 'Линия золота',
        'lane_icon': 'gold.svg',
        'template': 'meta.html',
        'output_name': 'gold_lane.html',
    },
    {
        'file_path': 'data/Exp Lane.csv',
        'title': 'Линия опыта',
        'lane_icon': 'exp.svg',
        'template': 'meta.html',
        'output_name': 'exp_lane.html',
    },
    {
        'file_path': 'data/Mid Lane.csv',
        'title': 'Мидеры',
        'lane_icon': 'mid.svg',
        'template': 'meta.html',
        'output_name': 'mid_lane.html',
    },
    {
        'file_path': 'data/Roam.csv',
        'title': 'Роумеры',
        'lane_icon': 'roam.svg',
        'template': 'meta.html',
        'output_name': 'roam_lane.html',
    },
    {
        'file_path': 'data/Jungle.csv',
        'title': 'Лесники',
        'lane_icon': 'jungle.svg',
        'template': 'meta.html',
        'output_name': 'jungle_lane.html',
    },
    {
        'file_path': 'data/ban_top.csv',
        'title': 'Тир лист запретов',
        'lane_icon': 'ban_logo.png',
        'template': 'ban.html',
        'output_name': 'ban_top.html',
    },
]


def make_html():
    env = Environment(loader=FileSystemLoader('browser/templates'))
    for lane_config in DATA_CONFIG:

        print(f"Создается HTML файл - {lane_config['output_name']}")

        df = pd.read_csv(lane_config['file_path'])
        template = env.get_template(lane_config['template'])

        context = lane_config.copy()
        context['heroes'] = df.to_dict('records')

        html_output = template.render(context)

        output_path = f'browser/outputs/{lane_config["output_name"]}'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)

if __name__ == "__main__":
    make_html()
