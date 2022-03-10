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
        case "octal":
            return validate_basic(last_count, new_count, 8)
        case "hex":
            return validate_basic(last_count, new_count, 16)
        case "powersof3":
            return validate_mult(last_count, new_count, 3)
        case "powersof2":
            return validate_mult(last_count, new_count, 2)
        case "no3":
            return validate_missing(last_count, new_count, 3)
        case "tugofwar":
            return validate_basic(last_count, new_count, 10) or \
                validate_backwards(last_count, new_count)
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

def validate_mult(last_count: str, new_count: str, coeff: int) -> bool:
    try:
        new_count = int(new_count)
        if last_count != '':
            last_count = int(last_count)
            return (new_count/last_count) == coeff
        else:
            return True
    except ValueError:
        return False

def validate_missing(last_count: str, new_count: str, target: str) -> bool:
    try:
        if target in new_count:
            return False
        new_count = int(new_count)
        if last_count != '':
            last_count = int(last_count)

            # TODO: Replace hacky solution
            while target in str(last_count + 1):
                last_count += 1
            
            return new_count == last_count + 1
        else:
            return True
    except ValueError:
        return False
