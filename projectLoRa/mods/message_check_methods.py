'''
like ENUMS to centrelize the config
'''

messageCodes = [
    ('ALIV', 1),
    ('KDIS', 2),
    ('ADDR', 3),
    ('POLL', 4),
]
messageCodes.sort()  # Sorts the list in-place

'''
returns the ENUM Number (was defined in the head of this code) when the message code was found 
'''


def checkMessage(message):
    global messageCodes
    try:
        return next(x for x in messageCodes if message[3] in x)
    except StopIteration:
        raise ValueError("No matching record found")


'''
expected an message array to check 
'''


def checkKoordinator(message):
    # koordinator hat 0000
    if message[1] == "0000":
        return 1
    else:
        return -1
