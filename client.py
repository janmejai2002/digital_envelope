from util import *
from constants import *
PUBLIC, PRIVATE = crypt_keygen()

def main():
    keygen_share(PUBLIC, "Client", "Server", HOST, KEY_EXCHANGE_PORT_CLIENT)
    server_pubkey = key_listener(HOST,KEY_EXCHANGE_PORT_SERVER)
    while True:
        sendEnv(server_pubkey, HOST, CLIENT_TO_SERVER, 'Client')
        recEnv(PRIVATE, HOST, SERVER_TO_CLIENT,  'Server')
if __name__ == "__main__":
    main()