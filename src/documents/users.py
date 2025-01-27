from beanie import Document


class User(Document):
    email: str
    password: str

    class Settings:
        name = 'users'
