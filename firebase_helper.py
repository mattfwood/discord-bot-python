import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("firebase-keys.json")
firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://discord-bot-db.firebaseio.com'}
)

ref = db.reference('/players')
# print(ref.get())


class fb:
    def get(path, data=None):
        return db.reference(path).get()

    def update(path, data):
        return db.reference(path).set(data)


if __name__ == "__main__":
    print(fb.get('/players'))
