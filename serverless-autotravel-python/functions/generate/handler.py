from __future__ import print_function

import json
import logging
import sys
import os
this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append("{0}/../lib".format(this_dir))
sys.path.append("{0}/../src".format(this_dir))
from jsonschema import validate
from generator.generator import convert_to_imacro

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    # input_json = json.dumps(event)
    with open(os.path.join(this_dir, '../resources/schema.json'), 'r') as myfile:
        schema = json.loads(myfile.read())
    try:
        validate(event, schema)
    except Exception as e:
        return "The input failed validation\n{0}".format(repr(e))
    try:
        output = convert_to_imacro(event)
    except Exception as e:
        return "An internal error occured during response generation\n{0}".format(repr(e))
    return output
