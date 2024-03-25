from spyre import server
import pandas as pd

class SetData(server.App):
    title = "NOAA Data Visualization"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'NOAA Data',
            "options": [{"label": "VCI", "value": "VCI"},
                        {"label": "TCI", "value": "TCI"},
                        {"label": "VHI", "value": "VHI"}],
            "key": 'ticker',
        },
        {
            "type": 'dropdown',
            "label": 'Area',
            "options": [{"label": "Вінницька", "value": "Вінницька"},
                        {"label": "Волинська", "value": "Волинська"},
                        {"label": "Дніпропетровська", "value": "Дніпропетровська"},
                        {"label": "Донецька", "value": "Донецька"},
                        {"label": "Житомирська", "value": "Житомирська"},
                        {"label": "Закарпатська", "value": "Закарпатська"},
                        {"label": "Запорізька", "value": "Запорізька"},
                        {"label": "Івано-Франківська", "value": "Івано-Франківська"},
                        {"label": "Київ", "value": "Київ"},
                        {"label": "Київська", "value": "Київська"},
                        {"label": "Кіровоградська", "value": "Кіровоградська"},
                        {"label": "Луганська", "value": "Луганська"},
                        {"label": "Львівська", "value": "Львівська"},
                        {"label": "Миколаївська", "value": "Миколаївська"},
                        {"label": "Одеська", "value": "Одеська"},
                        {"label": "Полтавська", "value": "Полтавська"},
                        {"label": "Рівенська", "value": "Рівенська"},
                        {"label": "Сумська", "value": "Сумська"},
                        {"label": "Тернопільська", "value": "Тернопільська"},
                        {"label": "Харківська", "value": "Харківська"},
                        {"label": "Херсонська", "value": "Херсонська"},
                        {"label": "Хмельницька", "value": "Хмельницька"},
                        {"label": "Черкаська", "value": "Черкаська"},
                        {"label": "Чернівецька", "value": "Чернівецька"},
                        {"label": "Чернігівська", "value": "Чернігівська"},
                        {"label": "Севастопіль", "value": "Севастопіль"},
                        {"label": "Республіка Крим", "value": "Республіка Крим"}],
            "key": 'area',
        },
        {
            "type": 'text',
            "label": 'Year',
            "key": 'year',
            "value": '',
        },
        {
            "type": 'text',
            "label": 'Week Range',
            "key": 'weekRange',
            "value": '',
        }
    ]

    controls = [{"type": "button",
                 "label": "Build",
                 "id": "update_data"}]

    tabs = ["Table", "Plot"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        data = pd.read_csv("df.csv")
        return data

    def getTable(self, params):
        df = self.getData(params)
        area = params['area']
        year = int(params['year'])
        weekRange = [int(x) for x in str(params['weekRange']).split('-')]

        searched_df = df[(df['Area'] == area) & (df['Year'] == year) & (df['Week'] >= weekRange[0]) & (df['Week'] <= weekRange[1])]
        searched_df = searched_df[['Year', 'Week', params['ticker'], 'Area']]
        return searched_df

    def getPlot(self, params):
        df = self.getData(params)
        area = params['area']
        year = int(params['year'])
        weekRange = [int(x) for x in str(params['weekRange']).split('-')]
        ticker = params['ticker']

        searched_data = df[(df['Area'] == area) & (df['Year'] == year) & (df['Week'] >= weekRange[0]) & (df['Week'] <= weekRange[1])]
        plt_obj = searched_data.plot(x='Week', y=ticker, figsize=(20, 10), grid=True)
        plt_obj.set_title(f"Графік для {area} області у {year} році для вказаного року та діапазону тижнів")
        plt_obj.set_ylabel("Значення")
        plt_obj.set_xlabel("Тижні")
        plot = plt_obj.get_figure()
        return plot


if __name__ == '__main__':
    app = SetData()
    app.launch()