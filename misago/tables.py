import sqlalchemy

from .avatars.types import AvatarType

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

user_groups = sqlalchemy.Table(
    "misago_user_groups",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("slug", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("css_suffix", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("ordering", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("is_default", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("is_guest", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("is_hidden", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("is_moderator", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("is_admin", sqlalchemy.Boolean, nullable=False),
)

user_groups_permissions = sqlalchemy.Table(
    "misago_user_groups_permissions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column(
        "group_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_user_groups.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column("permission", sqlalchemy.String(length=50), nullable=False),
)

users = sqlalchemy.Table(
    "misago_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
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
    sqlalchemy.Column("full_name", sqlalchemy.String(length=150), nullable=True),
    sqlalchemy.Column("password", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column(
        "group_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_user_groups.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    sqlalchemy.Column("acl_key", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("avatar_type", sqlalchemy.Enum(AvatarType), nullable=False),
    sqlalchemy.Column("avatars", sqlalchemy.JSON(), nullable=True),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("is_moderator", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("is_admin", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("joined_at", sqlalchemy.DateTime(timezone=True), nullable=False),
    sqlalchemy.Column("extra", sqlalchemy.JSON(), nullable=False),
)

sqlalchemy.Index(
    "misago_users_inactive",
    users.c.is_active,
    postgresql_where=users.c.is_active == False,  # pylint: disable=C0121
)
sqlalchemy.Index(
    "misago_users_moderators",
    users.c.is_moderator,
    postgresql_where=users.c.is_moderator == True,  # pylint: disable=C0121
)
sqlalchemy.Index(
    "misago_users_admins",
    users.c.is_admin,
    postgresql_where=users.c.is_admin == True,  # pylint: disable=C0121
)
sqlalchemy.Index(
    "misago_users_without_full_names",
    users.c.full_name,
    postgresql_where=users.c.full_name == None,  # pylint: disable=C0121
)
sqlalchemy.Index(
    "misago_users_slugs_search",
    users.c.slug,
    postgresql_ops={"slug": "gin_trgm_ops"},
    postgresql_using="gin",
)
sqlalchemy.Index(
    "misago_users_full_names_search",
    users.c.full_name,
    postgresql_ops={"full_name": "gin_trgm_ops"},
    postgresql_using="gin",
)

user_group_memberships = sqlalchemy.Table(
    "misago_user_group_memberships",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "group_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_user_groups.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column("is_main", sqlalchemy.Boolean, nullable=False, index=True),
)

categories = sqlalchemy.Table(
    "misago_categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column("type", sqlalchemy.Integer, nullable=False, index=True),
    sqlalchemy.Column(
        "parent_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_categories.id", ondelete="RESTRICT"),
        nullable=True,
    ),
    sqlalchemy.Column("depth", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("left", sqlalchemy.Integer, nullable=False, index=True),
    sqlalchemy.Column("right", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("slug", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("color", sqlalchemy.String(length=7), nullable=True),
    sqlalchemy.Column("icon", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column(
        "threads", sqlalchemy.Integer, server_default="0", nullable=False
    ),
    sqlalchemy.Column("posts", sqlalchemy.Integer, server_default="0", nullable=False),
    sqlalchemy.Column("is_closed", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("extra", sqlalchemy.JSON(), nullable=False),
)

threads = sqlalchemy.Table(
    "misago_threads",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column(
        "category_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_categories.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "first_post_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_posts.id", use_alter=True, ondelete="SET NULL"),
        nullable=True,
    ),
    sqlalchemy.Column(
        "starter_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_users.id", ondelete="SET NULL"),
        nullable=True,
    ),
    sqlalchemy.Column("starter_name", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column(
        "last_post_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_posts.id", use_alter=True, ondelete="SET NULL"),
        nullable=True,
    ),
    sqlalchemy.Column(
        "last_poster_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_users.id", ondelete="SET NULL"),
        nullable=True,
    ),
    sqlalchemy.Column(
        "last_poster_name", sqlalchemy.String(length=255), nullable=False
    ),
    sqlalchemy.Column("title", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("slug", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("started_at", sqlalchemy.DateTime(timezone=True), nullable=False),
    sqlalchemy.Column(
        "last_posted_at", sqlalchemy.DateTime(timezone=True), nullable=False
    ),
    sqlalchemy.Column(
        "replies", sqlalchemy.Integer, server_default="0", nullable=False
    ),
    sqlalchemy.Column("is_closed", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("extra", sqlalchemy.JSON(), nullable=False),
)

sqlalchemy.Index(
    "misago_threads_order", threads.c.last_post_id.desc(), threads.c.category_id
)

posts = sqlalchemy.Table(
    "misago_posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column(
        "category_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_categories.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "thread_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_threads.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "poster_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_users.id", ondelete="SET NULL"),
        nullable=True,
    ),
    sqlalchemy.Column("poster_name", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("markup", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("rich_text", sqlalchemy.JSON(), nullable=False),
    sqlalchemy.Column("edits", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("posted_at", sqlalchemy.DateTime(timezone=True), nullable=False),
    sqlalchemy.Column("extra", sqlalchemy.JSON(), nullable=False),
)

categories_permissions = sqlalchemy.Table(
    "misago_categories_permissions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column(
        "group_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_user_groups.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "category_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("misago_categories.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column("permission", sqlalchemy.String(length=50), nullable=False),
)

moderators = sqlalchemy.Table(
    "misago_moderators",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column(
        "category_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_categories.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "group_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_user_groups.id", ondelete="CASCADE"),
        nullable=True,
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("misago_users.id", ondelete="CASCADE"),
        nullable=True,
    ),
)

attachment_types = sqlalchemy.Table(
    "misago_attachment_types",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("extensions", sqlalchemy.JSON(), nullable=False),
    sqlalchemy.Column("mimetypes", sqlalchemy.JSON(), nullable=False),
    sqlalchemy.Column("size_limit", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column(
        "is_active", sqlalchemy.Boolean, server_default="true", nullable=False
    ),
)
