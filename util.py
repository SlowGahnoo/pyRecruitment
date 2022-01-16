def is_float(n):
    try:
        float(n)
        return True
    except ValueError:
        return False
