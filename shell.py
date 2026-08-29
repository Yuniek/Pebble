import pebble

env = pebble.Environment()
while True:
    text = input('pebble > ')

    if text == 'bye()': exit()


    try:
        result = pebble.run(text, env)
        if result is not None:
            print(result)
            
    except pebble.PebbleError as error:
        print(error)