import random

def encode(text):
    f = open('DO_NOT_MODIFY.txt', 'w')
    # Key = CX + 10D + E
    key = (random.randint(3, 7), random.randint(1, 9), random.randint(1, 9))
    errors = (random.randint(100, 999), random.randint(0, 9), random.randint(10000, 99999), key[1])
    code = str(errors[0]) + str(key[0]) + str(errors[1]) + str(key[1]) + str(errors[2]) + str(key[2]) + str(errors[3])

    f.write(code)
    f.write('\n')

    # Usable Characters : 32 - 122

    for char in text:
        new_position = (key[0] * ord(char) + 10 * key[1] + key[2])
        for i in range(0, 3):
            x = int(str(new_position)[i])
            if x > 3:
                f.write(chr(x + 10 * random.randint(3, 9)))
            else:
                f.write(chr(x + 10 * random.randint(4, 9)))
    f.close()


def decode():
    try:
        f = open('DO_NOT_MODIFY.txt', 'r')
        go = True
    except:
        print("This file does not exist. Therefore you cannot decode it.")
        go = False
    if go:
        text = f.read()
        if len(text) < 13:
            print("You can't decode this file because it is corrupted.")
        key = text[3] + text[5] + text[11]
        message = ""
        try:
            for i in range(1, int((len(text) - 14) / 3) + 1):
                pos_1 = int(str(ord(text[3 * i + 11]))[1])
                pos_2 = int(str(ord(text[3 * i + 12]))[1])
                pos_3 = int(str(ord(text[3 * i + 13]))[1])
                pos = 100 * pos_1 + 10 * pos_2 + pos_3
                char = (pos - int(key[2]) - 10 * int(key[1])) / int(key[0])
                message += chr(int(char))
            f.close()
            print (message)
            return message
        except:
            print("Your save is corrupted. You shouldn't have modified it.")


#while True:
#    choice = input("""What do you want to do:
#1 : Encode
#2 : Decode
#""")
#    if choice == "1":
#        text = input("Type your text : ")
#        encode(text)
#    if choice == "2":
#        decode()
#    elif choice == 'STOP' or choice == 'stop':
#        break
