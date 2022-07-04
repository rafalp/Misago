from typing import Any, Optional, Tuple

from sqlalchemy import BigInteger, Column, Integer, SmallInteger

DB_INT_COLUMN = (BigInteger, Integer, SmallInteger)


class ValidationError(ValueError):
    pass


def clean_first_last(data: dict, limit=int) -> Tuple[Optional[int], Optional[int]]:
    if not data.get("first") and not data.get("last"):
        raise ValidationError("You must provide either 'first' or 'last' argument.")

    first = data.get("first")
    last = data.get("last")

    if first is not None and last is not None:
        raise ValidationError(
            "'first' and 'last' arguments can't be used at same time."
        )

    if first is not None and first < 1:
        raise ValidationError("'first' can't be less than 1.")
    if last is not None and last < 1:
        raise ValidationError("'last' can't be less than 1.")

    if first and first > limit:
        raise ValidationError(f"'first' can't be greater than {limit}.")
    if last and last > limit:
        raise ValidationError(f"'last' can't be greater than {limit}.")

    return first, last


def clean_after_before(
    data: dict, db_col: Column
) -> Tuple[Optional[Any], Optional[Any]]:
    after = data.get("after")
    before = data.get("before")

    if after is not None and before is not None:
        raise ValidationError(
            "'after' and 'before' arguments can't be used at same time."
        )

    if isinstance(db_col.type, DB_INT_COLUMN):
        try:
            if after is not None:
                clean_after = int(after)
                if clean_after < 1:
                    raise ValidationError("'after' argument must be greater than 0.")
                return clean_after, None
            if before is not None:
                clean_before = int(before)
                if clean_before < 1:
                    raise ValidationError("'before' argument must be greater than 0.")
                return None, clean_before
        except (ValueError, TypeError):
            if after is not None:
                raise ValidationError("'after' argument must be a number.")
            if before is not None:
                raise ValidationError("'before' argument must be a number.")

    if after is not None:
        return str(after), None
    if before is not None:
        return None, str(before)

    return None, None
