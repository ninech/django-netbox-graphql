import json

def not_none(value):
    return value is not None

def set_and_save(fields, input, object):
    for field in fields:
        if not_none(input.get(field)):
            setattr(object, field, input.get(field))
    object.full_clean()
    object.save()
    return object

def print_result(result):
    print(json.dumps(result.data))
