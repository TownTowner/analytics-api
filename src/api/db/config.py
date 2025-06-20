import decouple

DATABASE_URL = str(decouple.config("DATABASE_URL", default=""))
DB_TIMEZONE = str(decouple.config("DB_TIMEZONE", default="UTC"))
