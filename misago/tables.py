import sqlalchemy

metadata = sqlalchemy.MetaData()

cache_versions = sqlalchemy.Table(
    "misago_cache_versions",
    metadata,
    sqlalchemy.Column("cache", sqlalchemy.String(length=32), primary_key=True),
    sqlalchemy.Column("version", sqlalchemy.String(length=8), nullable=False),
)

settings = sqlalchemy.Table(
    "misago_settings",
    metadata,
    sqlalchemy.Column("name", sqlalchemy.String(length=255), primary_key=True),
    sqlalchemy.Column("value", sqlalchemy.JSON(), nullable=False),
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
    sqlalchemy.Column(
        "email_hash", sqlalchemy.String(length=255), nullable=False, unique=True
    ),
    sqlalchemy.Column("password", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("is_deactivated", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("is_moderator", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("is_admin", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("joined_at", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("extra", sqlalchemy.JSON(), nullable=False),
)

sqlalchemy.Index(
    "users_deactivated",
    users.c.id,
    postgresql_where=users.c.is_deactivated == True,  # pylint: disable=C0121
)
sqlalchemy.Index(
    "users_moderators",
    users.c.id,
    postgresql_where=users.c.is_moderator == True,  # pylint: disable=C0121
)
sqlalchemy.Index(
    "users_admins",
    users.c.id,
    postgresql_where=users.c.is_admin == True,  # pylint: disable=C0121
)

categories = sqlalchemy.Table(
    "misago_categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("type", sqlalchemy.Integer, nullable=False, index=True),
    sqlalchemy.Column(
        "parent_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_categories.id"),
        nullable=True,
    ),
    sqlalchemy.Column("depth", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("left", sqlalchemy.Integer, nullable=False, index=True),
    sqlalchemy.Column("right", sqlalchemy.Integer, nullable=False),
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
