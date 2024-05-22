

# noinspection PyUnusedLocal
# friend_name = unicode string
def hello(friend_name):
    # validate parameter is a string
    if isinstance(friend_name, str):
        return f"Hello, {friend_name}"
    else:
        raise ValueError("parameter must be a string")


