def toCipher(plaintext):
    result = ""  #ciphertext
    s=3  #shift
    # to loop through the plain text
    for i in range(len(plaintext)):
        char = plaintext[i] #select char at index i
        if char ==' ':
            result+=char  #pass empty space as space to cypher
        elif (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)  # Encrypt uppercase
        else:
            result += chr((ord(char) + s - 97) % 26 + 97) # Encrypt lowercase
    print(f"Sending Cipher :  {result}")
    return result

def toPlaintext(ciphertext):
    result = "" #plaintext
    s=3  #shift
    # loop through the cipher text
    for i in range(len(ciphertext)):
        char = ciphertext[i] # select char at index i
        if char==' ':  # encrypt empty space as space
            result+=char
        elif (char.isupper()):
            result += chr((ord(char) - s-65) % 26 + 65) # Encrypt uppercase
        else:
            result += chr((ord(char) - s - 97) % 26 + 97)  # Encrypt lowercase
    return result