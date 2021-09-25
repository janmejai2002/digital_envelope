import socket,sys
from rsa_enc import *
def keygen_share(p_key, sender, receiver, h,p):
    """Function to share a key at specified host and port

    Args:
        p_key (tuple): public key
        sender (str): sender of key
        receiver (str): receiver of key
        h (str): Host ip for socket
        p (int): Port for the socket
    """
    key_message = f"Hi {receiver}. This is {sender}. Please send me your public key. Mine is {p_key}"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((h,p))
        s.sendall(key_message.encode('utf-8'))
        print(f"{sender} : {key_message}")

def key_listener(h,p):
    """Listen for keys on a host and port and parse them accordingly

    Args:
        h (str): host ip for communication
        p (int): port for the host ip

    Returns:
        tuple: public key
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((h,p))
        s.listen() 
        conn, addr = s.accept() 
        with conn:
            while True:
                data = conn.recv(1024)
                msg = data.decode('utf-8')
                if len(data)!=0:
                    pkey = eval(msg[msg.index("Mine is")+8::])
                if not data:
                    break
    return pkey

def toPlaintext(ciphertext,s):
    """convert ciphertext to plaintext

    Args:
        ciphertext (str): string of ciphertext
        s (int): key for caeser cipher

    Returns:
        str: plaintext
    """
    result = "" #plaintext
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
def toCipher(plaintext,s):
    """convert plaintext to ciphertext using ceaser cipher algorithm with key s

    Args:
        plaintext (str): plaintext
        s (int): key for caeser cipher

    Returns:
        str: ciphertext
    """
    result = ""  #ciphertext
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


def sendEnv(pub_key, host ,port, send):
    """Function for sending digital envelope at a given host and its port. The function uses asymmetric key engcryption algorithm RSA to encrypt random symmetric key. The digital envelope sent contains the encrypted symmetric key and ciphertext.

    Args:
        pkey (tuple): public key of envelope receiver
        host (str): host ip
        port (int): port
    """
    SHIFT=random.randint(1,26)
    wrap_symkey = encrypt(pub_key,str(SHIFT))
    ptext = input(f"{send} : ")
    ctext = toCipher(ptext.strip(),SHIFT)
    envelope = ctext+". The encrypted symmetric key is : "+str(wrap_symkey)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host,port))
        s.sendall(envelope.encode('utf-8'))
    if ptext == 'quitx': 
        print("Disposing ports and closing connection. Thank you")
        sys.exit(0)
    

def recEnv(priv_key, host, port, send):
    """Function to receive a digital envelope at a host and port, then decrypt it using private key of receiver.

    Args:
        host (str): host ip
        port (int): port
        priv_key (tuple): private key
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host,port))
        s.listen() 
        conn, addr = s.accept() 
        with conn:
            while True:
                data = conn.recv(1024)
                msg = data.decode('utf-8')
                if len(data)!=0:
                    message = msg[0:msg.index(". The encrypted"):].strip()
                    e_symkey = msg[msg.index("key is : ")+len("key is : ")::].strip()
                    shift = int(decrypt(priv_key,eval(e_symkey)))
                    dec_msg = toPlaintext(message,shift)
                    print(f"{send} : {dec_msg}")
                    if dec_msg=='quitx': 
                        print("Disposing ports and closing connection. Thank you")
                        sys.exit(0)
                if not data:
                    break
