from util import *
from constants import *
PUBLIC, PRIVATE = crypt_keygen()

def main():
    client_pubkey = key_listener(HOST, KEY_EXCHANGE_PORT_CLIENT)
    keygen_share(PUBLIC, "Server", "Client", HOST, KEY_EXCHANGE_PORT_SERVER)
    while True:
        recEnv(PRIVATE, HOST, CLIENT_TO_SERVER, 'Client')  
        sendEnv(client_pubkey, HOST, SERVER_TO_CLIENT, 'Server')  
if __name__ == "__main__":
    main()