import sqlalchemy

metadata = sqlalchemy.MetaData()

settings = sqlalchemy.Table(
    "misago_settings",
    metadata,
    sqlalchemy.Column("name", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("value", sqlalchemy.String),
)

users = sqlalchemy.Table(
    "misago_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=50), nullable=False),
    sqlalchemy.Column(
        "slug", sqlalchemy.String(length=50), nullable=False, unique=True
    ),
    sqlalchemy.Column(
        "email", sqlalchemy.String(length=255), nullable=False, unique=True
    ),
    sqlalchemy.Column("password", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("is_moderator", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("joined_at", sqlalchemy.DateTime, nullable=False),
)

categories = sqlalchemy.Table(
    "misago_categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("slug", sqlalchemy.String(length=255), nullable=False),
)

threads = sqlalchemy.Table(
    "misago_threads",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "category_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_categories.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "starter_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_users.id"),
        nullable=True,
    ),
    sqlalchemy.Column("starter_name", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column(
        "last_poster_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_users.id"),
        nullable=True,
    ),
    sqlalchemy.Column(
        "last_poster_name", sqlalchemy.String(length=255), nullable=False
    ),
    sqlalchemy.Column("title", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("slug", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("started_at", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column(
        "last_posted_at", sqlalchemy.DateTime, nullable=False, index=True
    ),
)

posts = sqlalchemy.Table(
    "misago_posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "category_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_categories.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "thread_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_threads.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "poster_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_users.id"),
        nullable=True,
    ),
    sqlalchemy.Column("poster_name", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("body", sqlalchemy.JSON, nullable=False),
    sqlalchemy.Column("posted_at", sqlalchemy.DateTime, nullable=False),
)
