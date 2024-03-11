import pandas as pd
import os

directory = 'raw'
files = files = sorted(os.listdir(directory), key=lambda x: int(x.split('_')[-1].split('.')[0]))
uncombined_df = []
headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'Area']
i = 1

index_changer = {
    1:'Черкаська', 2:'Чернігівська', 3:'Чернівецька', 4:'Республіка Крим', 5:'Дніпропетровська',
    6:'Донецька', 7:'Івано-Франківська', 8:'Харківська', 9:'Херсонська', 10:'Хмельницька',
    11:'Київська', 12:'Київ', 13:'Кіровоградська', 14:'Луганська', 15:'Львівська',
    16:'Миколаївська', 17:'Одеська', 18:'Полтавська', 19:'Рівеньска', 20:'Севастопіль',
    21:'Сумьска', 22:'Тернопільська', 23:'Закарпатська', 24:'Вінницька', 25:'Волинська',
    26:'Запорізька', 27:'Житомирська',
}



for file in files:
    file_path = os.path.join(directory, file)
    dataframe = pd.read_csv(file_path, header = 1, names = headers)
    dataframe.drop(dataframe.index[-1], inplace=True)
    dataframe['Area'] = i
    i += 1

    dataframe = dataframe.drop(dataframe.loc[dataframe['VHI'] == -1].index)
    dataframe['Area'] = dataframe['Area'].replace({index: area for index, area in index_changer.items()})

    uncombined_df.append(dataframe)

df = pd.concat(uncombined_df, ignore_index=True)



def VHI_of_year_finder(area, year):
    finded = df[(df["Area"] == area) & (df["Year"] == str(year))]
    for index, row in finded.iterrows():
        print(f"Тиждень: {row['Week']}, VHI: {row['VHI']}")

    min_v = df[(df['Year'].astype(str) == str(year)) & (df["Area"] == area)]['VHI'].min()
    print('Найменший показник VHI у', area, 'за', year, 'рік: ', min_v)
    max_v = df[(df['Year'].astype(str) == str(year)) & (df["Area"] == area)]['VHI'].max()
    print('Найбільший показник VHI у', area, 'за', year, 'рік: ', max_v)


def VHI_of_range_finder(areas, start_year, end_year):
    for year in range(start_year, end_year + 1):
        print(f"Рік: {year}")
        for area in areas:
            filtered_data = df[(df['Year'] == str(year)) & (df['Area'] == area)]
            print(f"Область: {area}")
            for index, row in filtered_data.iterrows():
                print(f"Тиждень: {row['Week']}, VHI: {row['VHI']}")
            print()
        print()


def drought_finder(percentage):
    for year in df['Year'].unique():
        drought_counter = 0
        slight_drought_counter = 0
        for area in df['Area'].unique():
            area_data = df[(df['Year'] == year) & (df['Area'] == area)]
            if (area_data['VHI'] < 15).any():
                drought_counter += 1
            elif (area_data['VHI'] < 35).any():
                slight_drought_counter += 1
        if drought_counter/27 * 100 > percentage:
            print(f'Рік, коли Екстримальні посухи торкнулися більше {percentage}% областей по Україні: ', year)
        if slight_drought_counter/27 * 100 > percentage:
            print(f'Рік, коли Помірні посухи торкнулися більше {percentage}% областей по Україні: ', year)



#VHI_of_year_finder('Черкаська', 1987)
#VHI_of_range_finder(['Черкаська', 'Запорізька'], 1987, 1989)
#drought_finder(20)
