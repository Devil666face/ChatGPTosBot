from peewee import SqliteDatabase, Model, CharField, IntegerField

db = SqliteDatabase("database.db")


class Person(Model):
    name = CharField()
    age = IntegerField()

    class Meta:
        database = db


db.create_tables([Person])

person = Person(name="John", age=30)
person.save()

query = Person.select().where(Person.age > 20)
for person in query:
    print(person.name)
