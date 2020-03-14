import typing
from contextvars import ContextVar

from databases.core import (
    CONNECT_EXTRA,
    DISCONNECT_EXTRA,
    Connection as BaseConnection,
    Database as BaseDatabase,
    DatabaseURL,
    Transaction,
    logger,
)
from databases.importer import import_from_string
from databases.interfaces import DatabaseBackend


class Database(BaseDatabase):
    def __init__(
        self,
        url: typing.Union[str, "DatabaseURL"],
        *,
        force_rollback: bool = False,
        **options: typing.Any,
    ):
        self.url = DatabaseURL(url)
        self.options = options
        self.is_connected = False

        self._force_rollback = force_rollback

        backend_str = self.SUPPORTED_BACKENDS[self.url.dialect]
        backend_cls = import_from_string(backend_str)
        assert issubclass(backend_cls, DatabaseBackend)
        self._backend = backend_cls(self.url, **self.options)

        # Connections are stored as task-local state.
        self._connection_context = ContextVar("connection_context")  # type: ContextVar

        # When `force_rollback=True` is used, we use a single global
        # connection, within a transaction that always rolls back.
        self._global_connection: typing.Optional["Connection"] = None
        self._global_transaction: typing.Optional[Transaction] = None

    async def connect(self) -> None:
        """
        Establish the connection pool.
        """
        assert not self.is_connected, "Already connected."

        await self._backend.connect()
        logger.info(
            "Connected to database %s", self.url.obscure_password, extra=CONNECT_EXTRA
        )
        self.is_connected = True

        if self._force_rollback:
            self._global_connection = Connection(self._backend)
            self._global_transaction = self._global_connection.transaction(
                force_rollback=True
            )

            await self._global_transaction.__aenter__()

    async def disconnect(self) -> None:
        """
        Close all connections in the connection pool.
        """
        assert self.is_connected, "Already disconnected."

        if self._force_rollback:
            assert self._global_transaction is not None
            await self._global_transaction.__aexit__()

        await self._backend.disconnect()
        logger.info(
            "Disconnected from database %s",
            self.url.obscure_password,
            extra=DISCONNECT_EXTRA,
        )
        self.is_connected = False


class Connection(BaseConnection):
    async def iterate(
        self, query, values=None
    ) -> typing.AsyncGenerator[typing.Any, None]:
        async with self.transaction():
            async for record in self._connection.iterate(
                self._build_query(query, values)
            ):
                yield record
