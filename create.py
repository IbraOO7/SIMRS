from app import Login, db

user = Login('adminese','admin12345')
db.session.add(user)
db.session.commit()
