import cleverbotfree.cbfree

cb = cleverbotfree.cbfree.Cleverbot()


def chat():
    cb.browser.get(cb.url)
    while True:
        cb.get_form()
        user_input = input("You: ")
        if user_input == 'done':
            break
        cb.send_input(user_input)
        response = cb.get_response()
        print("Bot: " + response)
    cb.browser.close()


chat()
