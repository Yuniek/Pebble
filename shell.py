import pebble

while True:
    text = input('pebble > ')

    if text == 'bye()': exit()

    try:
        result = pebble.run(text)
        if result is not None:
            print(result)
            
    except pebble.PebbleError as error:
        print(error)