import requests
import os
import json
from dateutil.parser import parse
from datetime import datetime, timedelta
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# Begin Private File Paths
def _ACCOUNT_ID():
    return '132591'

def __PRIVATE_PATH():
    return os.path.join(os.path.dirname(__file__),
                        'private')


def __PUBLIC_KEY_PATH():
    return os.path.join(__PRIVATE_PATH(),'keys', 'rsa_public.pem')


def __PRIVATE_KEY_PATH():
    return os.path.join(__PRIVATE_PATH(),'keys', 'private_rsa_key.pem')


def __REFRESH_TOKEN_PATH():
    return os.path.join(__PRIVATE_PATH(), 'tokens', 'refresh_token.md')


def __ACCESS_TOKEN_PATH():
    return os.path.join(__PRIVATE_PATH(), 'tokens', 'access_token.md')


# End Private File Paths

# This is the encryption code used in the key files
def __PRIVATE_CODE():
    return 'EMMA@#!@WATSON@#!@HASH'


# Start Encryption Functions

def __create_encryption_key(passcode):
    key = RSA.generate(2048)
    encrypted_key = key.exportKey(passphrase=passcode, pkcs=8,
                                  protection="scryptAndAES128-CBC")
    with open(__PRIVATE_KEY_PATH(), 'wb') as f:
        f.write(encrypted_key)
    with open(__PUBLIC_KEY_PATH(), 'wb') as f:
        f.write(key.publickey().exportKey())


def __encrypt_data(outfile_path, keyfile_path,data):
    with open(outfile_path, 'wb') as out_file:
        recipient_key = RSA.import_key(
            open(keyfile_path).read())
        session_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        out_file.write(cipher_rsa.encrypt(session_key))
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        out_file.write(cipher_aes.nonce)
        out_file.write(tag)
        out_file.write(ciphertext)


def __decrypt_data(encrypted_path, key_path, passcode):
    with open(encrypted_path, 'rb') as fobj:
        private_key = RSA.import_key(
            open(key_path).read(),
            passphrase=passcode)
        enc_session_key, nonce, tag, ciphertext = [ fobj.read(x)
                                                    for x in (private_key.size_in_bytes(),
                                                    16, 16, -1) ]
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return data.decode()


def __create_refresh_data(client_id, client_secret, refresh_token):
    __encrypt_data(__REFRESH_TOKEN_PATH(), __PUBLIC_KEY_PATH(),
                   "".join([refresh_token + ',',
                    client_secret + ',',
                    client_id]).encode())


# End Encryption Function
# Start Token Update and Access Function

def __refresh_access_token():
    if os.path.exists(__ACCESS_TOKEN_PATH()) and os.path.exists(__REFRESH_TOKEN_PATH()):
        refresh_data = __decrypt_data(__REFRESH_TOKEN_PATH(),
                                      __PRIVATE_KEY_PATH(),
                                      __PRIVATE_CODE()).strip('\n').split(',')
        payload = {
            'refresh_token': refresh_data[0],
            'client_secret': refresh_data[1],
            'client_id': refresh_data[2],
            'grant_type': 'refresh_token',
        }
        token_data = requests.post(
            'https://cloud.merchantos.com/oauth/access_token.php',
            data=payload).json()
        outdata = "".join(
            [token_data['access_token'] + ',',
            datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ',',
            token_data['scope'].split(' ')[0] + ',',
            token_data['scope'].split(' ')[1].strip('systemuserid:')
            + ',']).encode()
        __encrypt_data(__ACCESS_TOKEN_PATH(), __PUBLIC_KEY_PATH(), outdata)
    else:
        print('NO SUCH FILE FOUND')
    return


def _get_access_token():
    if os.path.exists(__ACCESS_TOKEN_PATH()):
        token_file = open(__ACCESS_TOKEN_PATH(), 'r')
        content = __decrypt_data(__ACCESS_TOKEN_PATH(),
                                 __PRIVATE_KEY_PATH(),
                                 __PRIVATE_CODE()).split(',')
        try:
            token_time = datetime.strptime(content[1].strip('\n'),
                                                    "%Y-%m-%d %H:%M:%S")
            if token_time > datetime.now() - timedelta(hours = 1):
                return content[0].strip('\n')
            else:
                __refresh_access_token()
                _get_access_token()
        except Exception:
            __refresh_access_token()
            _get_access_token()
        token_file.close()
    else:
        print('NO SUCH FILE FOUND')
