

# noinspection PyUnusedLocal
# friend_name = unicode string
def hello(friend_name):
    msg = ''
    # validate parameter is a string
    if isinstance(friend_name, str):
        msg = f"Hello, {friend_name}!"
    else:
        msg = "Hello, World!"
    return msg



