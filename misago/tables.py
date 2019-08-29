import sqlalchemy

metadata = sqlalchemy.MetaData()

settings = sqlalchemy.Table(
    "settings",
    metadata,
    sqlalchemy.Column("name", sqlalchemy.String, primary_key=True, nullable=False),
    sqlalchemy.Column("value", sqlalchemy.String),
)
