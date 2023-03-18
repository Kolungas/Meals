import pandas as pd


class ProductList:
    def __init__(self, name='Foods'):
        self.name = name
        self.products = self.read_from_csv()
        self.tags = set(self.products['Теги'])

    def read_from_csv(self, file=None):
        if file is None:
            file = 'data/' + self.name + '.csv'
        df = pd.read_csv(file, index_col=0)
        #TODO: add check for same names
        return df

    def write_to_csv(self, file=None):
        if file is None:
            file = 'data/' + self.name + '.csv'
        self.products.to_csv(file)

    def add_product(self, name, tag, av=True, shop=False):
        new_product = pd.DataFrame({'Назва': name, 'Наявність': av, 'Покупка': shop}, index=[0])

        if tag in self.tags:
            new_product['Теги'] = tag
        else:
            print('Вказано неіснуючий тег!')
            return

        self.products = pd.concat([self.products, new_product], ignore_index=True)

    def print_list(self, subset=None, sort_by='Назва'):
        df = self.products.sort_values([sort_by])

        if subset is not None:
            for key in subset.keys():
                df = df[df[key] == subset[key]]

        df.reset_index(inplace=True, drop=True)
        return df

    def rename_product(self, old_name, new_name):
        if new_name in self.products['Назва'].values:
            print('Продукт з таким іменем уже існує!')
            return
        if old_name in self.products['Назва'].values:
            self.products['Назва'] = self.products['Назва'].replace([old_name], new_name)
        else:
            print('Продукт з таким іменем відсутній!')
            return

    def change_tag(self, name, new_tag):
        if name in self.products['Назва'].values:
            ind = self.products[self.products['Назва'] == name].index
            if new_tag in self.tags:
                self.products.loc[ind,'Теги'] = new_tag
            else:
                print(f'Тег {new_tag} відсутній у списку!')
                return
        else:
            print('Продукт з таким іменем відсутній!')
            return

    def change_availability(self, name):
        if name in self.products['Назва'].values:
            ind = self.products[self.products['Назва'] == name].index

            if False in self.products.loc[ind, 'Наявність'].values:
                self.products.loc[ind, 'Наявність'] = True
            else:
                self.products.loc[ind, 'Наявність'] = False
        else:
            print('Продукт з таким іменем відсутній!')
            return

    def change_shopping(self, name):
        if name in self.products['Назва'].values:
            ind = self.products[self.products['Назва'] == name].index

            if False in self.products.loc[ind, 'Покупка'].values:
                self.products.loc[ind, 'Покупка'] = True
            else:
                self.products.loc[ind, 'Покупка'] = False
        else:
            print('Продукт з таким іменем відсутній!')
            return


def read_meal_csv(name):
    read_dict = {}
    with open(name) as f:
        reader = pd.read_csv(f)
        for row in reader:
            if row[0] != '\ufeffName':
                read_dict[row[0]] = {'Teg': row[6], 
                                     'Availability': True if row[2] == 'Yes' else False,
                                     'Ingradients': row[1],
                                     'Link': row[3],
                                     'Time of day': row[4],
                                     'Cooking': row[5]
                }
    return read_dict


if __name__ == '__main__':
    r = ProductList('Foods')
    r.read_from_csv()
    r.add_product('Шоколад', 'Інше')
    r.change_shopping('Шпроти')
    d = r.print_list()
    print(d)
