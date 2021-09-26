def validate_string(*input):
    for str in input:
        if not(str and not str.isspace()):
            return False
    return True