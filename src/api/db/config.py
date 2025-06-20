import decouple

DATABASE_URL = str(decouple.config("DATABASE_URL"))
