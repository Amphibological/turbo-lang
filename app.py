from flask import Flask, render_template, url_for, request, redirect

from core.interpreter import interpret, lex  # TODO REMOVE LEX
from core.utils import Stack
import core.io as io

app = Flask(__name__)

DEBUG = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    program = request.form['code']
    program_input = request.form['input']
    program_args = request.form['args'].splitlines()

    url = f"{url_for('execute_code')}?code={program}"
    if program_input:
        url += '&input=' + program_input
    for index, text in enumerate(program_args):
        url += f'&arg{index}={text}'
    return redirect(url)


@app.route('/code')
def execute_code():
    program = request.args.get('code', '')
    program_input = request.args.get('input', '')
    program_args = []
    for i in range(10):
        try:
            program_args.append(request.args[f'arg{i}'])
        except KeyError:
            break
    
    output_class = 'no-error'

    if DEBUG:
        try:
            io.clean()
            io.input_buf = program_input
            io.args = program_args

            program_output = str(lex(program))
            program_output += '\n'
            stack = Stack()
            interpret(program, stack)
            program_output += io.output_buf
            program_output += '\n'
            program_output += str(stack)
            print(io.output_buf)
        except SyntaxError as e:
            program_output = e.msg
            output_class = 'error'
    else:
        try:
            io.clean()
            io.input_buf = program_input
            io.args = program_args

            interpret(program, Stack())
            program_output = io.output_buf  # from interpreter.
        except SyntaxError as e:
            program_output = e.msg
            output_class = 'error'

    return render_template('index.html',
                           output=program_output, 
                           program=program, 
                           input=program_input,
                           args='\n'.join(program_args),
                           output_class=output_class)