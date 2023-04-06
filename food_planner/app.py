from flask import Flask
from food_planner.main import ProductList

app = Flask(__name__)


@app.route('/')
def display_list():
    r = ProductList('Foods')
    r.read_from_csv()
    r.add_product('Шоколад', 'Інше')
    r.change_shopping('Шпроти')
    return r.print_list().to_html()
