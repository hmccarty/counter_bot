"""
Implements various counting types and ensures a count is valid.
"""

def validate_count(count_type: str, last_count: str, new_count: str) -> bool:
    match count_type:
        case "basic":
            return validate_basic(last_count, new_count, 10)
        case "backwards":
            return validate_backwards(last_count, new_count)
        case "binary":
            return validate_basic(last_count, new_count, 2)
        case _:
            return False

def validate_basic(last_count: str, new_count: str, base: int) -> bool:
    try:
        new_count = int(new_count, base)
        if last_count != '':
            last_count = int(last_count, base)
            return (new_count - last_count) == 1
        else:

            return True
    except ValueError:
        return False

def validate_backwards(last_count: str, new_count: str) -> bool:
    try:
        new_count = int(new_count)
        if last_count != '':
            last_count = int(last_count)
            return (new_count - last_count) == -1
        else:

            return True
    except ValueError:
        return False