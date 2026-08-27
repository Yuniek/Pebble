import pebble

while True:
    text = input('pebble > ')
    if text == 'bye()': exit()
    result = pebble.run(text)
    if result is not None:print(result)
