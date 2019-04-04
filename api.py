from flask import Flask, request, jsonify

from async.execute import execute_command_task
from async.commands import commands_fns
from utils.helpers import logger

app = Flask(__name__)


@app.route('/', methods=['GET'])
def dummy_index():
    return jsonify({"success": True})


@app.route('/commands/<command_name>', methods=['GET'])
def api_for_command(command_name):
    data = {'command': command_name, 'args': request.args.to_dict()}
    logger.info(f'Received with [{data}]')
    command_exists = command_name in commands_fns.keys()
    if command_exists:
        execute_command_task(data, None)
    return jsonify({"success": command_exists})


if __name__ == '__main__':
    app.run()
