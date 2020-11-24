from flask import abort

def check_for_required_values(data,keys):
    """
    Check if requested fields are available
    """
    errors = ''
    for each in keys:
        if not data.get(each):
            errors+=each+', '
    if len(errors)>2:
        abort(400, description=errors[:-2]+' fields are missing and are required.')

