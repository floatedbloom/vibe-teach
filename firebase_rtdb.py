# pip install firebase-admin python-dotenv

import firebase_admin
from firebase_admin import credentials, db
import os
import base64
import json

from dotenv import load_dotenv
load_dotenv()

def add_base64_padding(encoded_str):
    """Ensure the Base64 string has proper padding."""
    missing_padding = len(encoded_str) % 4
    if missing_padding:
        encoded_str += "=" * (4 - missing_padding)
    return encoded_str

if __name__ == '__main__':

    input('(Warning) Will reset .env file. Enter to continue. Ctrl-C to quit.')
    print('Open Project Overview > Service accounts > Firebase Admin SDK')
    print('Paste JSON file here')
    lines = []
    while True:
        line = input()
        if not line:
            if lines: break
            continue
        lines.append(line)
    s = '\n'.join(lines)
    print(len(lines), 'lines found')
    with open('.env', 'ab') as f:
        f.write(b'RTDB_KEY='+base64.b64encode(s.encode()))
    print('Written to RTDB_KEY in .env. Now all you need to do is modify databaseURL in this file.')

else:

    # Get the Base64-encoded key from the environment variable
    rtdb_key = os.getenv('RTDB_KEY')

    if not rtdb_key:
        raise ValueError("RTDB_KEY environment variable is not set.")

    # Add padding to the Base64 string if necessary
    rtdb_key = add_base64_padding(rtdb_key)

    # Decode the Base64 string and load the JSON
    _cert = json.loads(base64.b64decode(rtdb_key).decode())

    # Ensure `app` is defined globally for use when the script is imported
    if not firebase_admin._apps:
        app = firebase_admin.initialize_app(
            credentials.Certificate(_cert),
            {'databaseURL': 'https://fir-demo-6e298-default-rtdb.firebaseio.com'},
        )
    else:
        app = firebase_admin.get_app()  # Retrieve the already initialized app

    # Expose the Firebase reference for other modules
    firebase_ref = db.reference('/', app)