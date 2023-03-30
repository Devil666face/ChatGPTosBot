from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    BooleanField,
    TextField,
    DoesNotExist,
)

# from functools import lru_cache

db = SqliteDatabase("database.db")


class User(Model):
    id = IntegerField(primary_key=True)
    username = CharField(default="none")
    allow = BooleanField(default=False)
    query_count = IntegerField(default=0)
    last_ask = TextField(default="none")
    last_answer = TextField(default="none")

    class Meta:
        database = db

    @staticmethod
    def is_have_user(id: int, username: str) -> bool:
        if not User.select().where(User.id == id).exists():
            User.create(id=id, username=username).save()
            return True
        return False

    @staticmethod
    # @lru_cache(maxsize=None)
    def is_allow_user(id: int) -> bool:
        try:
            return User.get(id=id).allow
        except DoesNotExist:
            return False

    @staticmethod
    def set_allow_user(id: int) -> bool:
        # User.is_allow_user.cache_clear()
        obj = User.get(id=id)
        obj.allow = True
        obj.save()
        return True

    @staticmethod
    def ask(id: int, ask: str, answer: str) -> bool:
        obj = User.get(id=id)
        obj.query_count += 1
        obj.last_ask = ask
        obj.last_answer = answer
        obj.save()
        return True

    @staticmethod
    def get_last_ask(id: int) -> str:
        return User.get(id=id).last_ask

    @staticmethod
    def get_last_answer(id: int) -> str:
        return User.get(id=id).last_answer


def init_models():
    db.create_tables([User])
