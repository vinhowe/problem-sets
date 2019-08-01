"""
Main file to be split into smaller components once proof of concept proves the concept
"""
import os
from json import dumps, loads
from typing import List
from uuid import uuid4

from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS

import problem_sets as sets
from problem_sets import Environment, static, initialize, GenProblem
from problem_sets.static import StaticProblemEntity
from problem_sets.static.static_content import StaticContent, StaticContentType
from problem_sets.static.static_problem_set import StaticProblemSet

app = Flask(__name__, static_url_path='')
CORS(app)

UPLOAD_FOLDER = os.path.realpath(os.path.join(__file__, os.path.pardir, 'static_data', 'temp'))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# We need to have the option to ask multiple questions about one piece of information
# So we could have a function that asks different things about functions
# a) what is the absolute minimum?
# b) what are the x-intercepts, if any?
# c) what is the domain of this function?
# Et cetera...

# Additionally, we need to define a format that uses JSON nodes, so we can display elements like graphs
# Any widgets we define will need to have handlers on the client side.


def format_arg_key(arg):
    return arg.replace("<br>", "").replace("-", "_")


def format_arg(arg):
    return arg.replace("<br>", "")


@app.route("/api/problem/<set_id>")
def problem(set_id):
    # args = request.args.to_dict()
    # args_formatted = {}
    # for arg_key in args:
    #     arg_formatted = format_arg_key(arg_key)
    #     arg_value_formatted = format_arg(args[arg_key])
    #     args_formatted[arg_formatted] = arg_value_formatted

    response = sets.problem(set_id)
    response_serialized = response.serialize()

    if isinstance(response, GenProblem):
        print(dumps(response.debug_info, indent=4, separators=(",", ": ")))

    print(response_serialized)

    return jsonify(response_serialized)


@app.route("/static/images/<path:path>")
def images(path):
    return send_from_directory('static_data/images/', path)


@app.route("/api/static/sets", methods=['GET', 'POST'])
def static_sets():
    if request.method == 'POST':
        set_id = request.form['id']
        # TODO Make this not required
        source = None
        if 'source' in request.form:
            source = request.form['source']

        instruction_contents = []

        answer_contents = []

        if 'answers[]' in request.form:
            answers_info = request.form.getlist('answers[]')

            answers_images_info = request.files.getlist(
                'answersImages[]') if 'answersImages[]' in request.files else None

            answer_contents = decode_static_content_form_data_list(answers_info, answers_images_info)

        if 'instructions[]' in request.form:
            instructions_info = request.form.getlist('instructions[]')

            instructions_images_info = request.files.getlist(
                'instructionsImages[]') if 'instructionsImages[]' in request.files else None

            instruction_contents = decode_static_content_form_data_list(instructions_info, instructions_images_info)

        static_problem_set = StaticProblemSet(set_id, source, instruction_contents, answer_contents)

        # noinspection PyBroadException
        try:
            static.create_static_problem_set(static_problem_set)
        except Exception as e:
            return str(e), 405

        return Response(status=200)


@app.route('/api/static/sets/<set_id>', methods=['GET', 'PUT'])
def static_set(set_id: str):
    if request.method == 'GET':
        static_set = static.get_static_problem_set(set_id)
        return static_set.serialize()


@app.route('/api/static/problems', methods=['GET', 'POST'])
def static_problems():
    if request.method == 'POST':
        set_id = request.form['setId']

        if 'content' not in request.files:
            return 'no content in problem', 405

        image = request.files['content']

        static_content = static_content_from_image_upload(image)

        static_problem = StaticProblemEntity(set_id, False, [static_content])

        # try:
        static.create_problem(static_problem)
        # except Exception as e:
        #     return str(e), 405

        return Response(status=200)


def decode_static_content_form_data_list(static_form_data: list, files_form_data: list):
    if len(static_form_data) == 0:
        return

    static_contents: List[StaticContent] = []

    # Decode JSON
    static_form_data = list(loads(item) for item in static_form_data)

    for instruction_info in static_form_data:
        if instruction_info['type'] == "text":
            static_contents.append(StaticContent(StaticContentType.text, instruction_info['value']))
        elif instruction_info['type'] == "image":
            static_content = static_content_from_image_upload(files_form_data.pop(0))
            static_contents.append(static_content)

    return static_contents


def static_content_from_image_upload(image):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{str(uuid4()).replace('-', '')}.png")
    image.save(image_path)

    with open(image_path, "rb") as temp_image:
        data = temp_image.read()

    image_bytes = bytes(data)

    try:
        os.remove(image_path)
    except OSError as e:
        print(e)

    return StaticContent(StaticContentType.image, image_bytes)


def main():
    print('initializing server')
    initialize(Environment.debug)
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000, debug=True)


main()
