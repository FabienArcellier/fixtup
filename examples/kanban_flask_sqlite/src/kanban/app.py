from typing import Optional

from flask import Flask, jsonify, abort, request, Response

from kanban.database import db_connect, db_session
from kanban.model import WorkItem, BoardColumn

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
    work_item: Optional[WorkItem] = WorkItem.query.filter(WorkItem.pid == id).first()
    if work_item is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(work_item)

    if request.method == 'PUT':
        # update work_item object from payload
        payload = request.json
        column_pid: Optional[int] = payload.get('column', None)
        if column_pid is not None and column_pid != work_item.column:
            board_column: BoardColumn = BoardColumn.query.filter(BoardColumn.pid == column_pid).first()
            if board_column is None:
                abort(Response('board column must exists', 500))

            # check the rule about wip
            current_wip = WorkItem.query.filter(WorkItem.column == column_pid).count()
            if current_wip >= board_column.wip_limit:
                return jsonify({'ok': False})

            work_item.column = column_pid

        title: Optional[str] = payload.get('title', None)
        if title is not None:
            work_item.title = title

        description: Optional[str] = payload.get('description', None)
        if description is not None:
            work_item.description = description

        dbsession = db_session()
        dbsession.commit()

        return jsonify({'ok': True})

    abort(400)


@app.before_request
def init_session():
    db_connect()


@app.teardown_appcontext
def shutdown_session(exception=None):
    dbsession = db_session()
    if dbsession is not None:
        dbsession.remove()


if __name__ == "__main__":
    app.run(debug=True)
