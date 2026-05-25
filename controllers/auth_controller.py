from models.User import User
class authController :
    def __init__(self,db):
        self.db=db

    def connecter(self,user_id):
        return self.db.find_user(user_id)
    
    def creer_compte(self,name,email):
        u=User(name,email)
        self.db.users.append(u)
        self.db.save_user(u)
        return u

