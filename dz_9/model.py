from mongoengine import Document
from mongoengine.fields import ListField, StringField, ReferenceField
from mongoengine import connect
import configparser

config = configparser.ConfigParser()
connect(host=f"""mongodb+srv://sturenko4:31122014@sturenko4.e02me8x.mongodb.net/base.authors?retryWrites=true&w=majority&appName=sturenko4""", ssl=True)

class Authors(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors)
    quote = StringField()