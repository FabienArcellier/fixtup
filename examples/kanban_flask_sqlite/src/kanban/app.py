from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/column', methods=['GET', 'POST'])
def column():
    pass


@app.route('/column/<id>', methods=['GET', 'PUT', 'DELETE'])
def column_id(id: int):
    pass


@app.route('/work_item', methods=['GET', 'POST'])
def work_item():
    pass


@app.route('/work_item/<id>', methods=['GET', 'PUT', 'DELETE'])
def work_item_id(id: int):
    pass


if __name__ == "__main__":
    app.run(debug=True)
