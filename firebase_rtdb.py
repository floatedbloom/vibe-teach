# pip install firebase-admin python-dotenv

import firebase_admin
from firebase_admin import credentials, db
import os
import base64
import json

from dotenv import load_dotenv
load_dotenv()

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

    _cert = json.loads(base64.b64decode(os.getenv('RTDB_KEY')).decode())

    app = firebase_admin.initialize_app(
        credentials.Certificate(_cert),
        {'databaseURL': 'https://fir-demo-6e298-default-rtdb.firebaseio.com'},
        name='firebase-demo'
    )

    ref = db.reference('/', app)