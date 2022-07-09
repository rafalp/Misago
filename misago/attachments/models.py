from dataclasses import dataclass
from typing import Any, Awaitable, Dict, List, Optional

from ..database import Model, register_model
from ..tables import attachment_types


@register_model("AttachmentType", attachment_types)
@dataclass
class AttachmentType(Model):
    id: int
    name: str
    extensions: List[str]
    mimetypes: List[str]
    size_limit: Optional[int]
    is_active: bool

    @classmethod
    def create(
        cls,
        name: str,
        extensions: List[str],
        *,
        mimetypes: Optional[List[str]] = None,
        size_limit: Optional[int] = None,
        is_active: bool = True,
    ) -> Awaitable["AttachmentType"]:
        data: Dict[str, Any] = {
            "name": name,
            "extensions": clean_list_value(extensions),
            "mimetypes": clean_list_value(mimetypes),
            "size_limit": size_limit if size_limit and size_limit > 0 else None,
            "is_active": is_active,
        }

        return cls.query.insert(**data)

    async def update(
        self,
        *,
        name: Optional[str] = None,
        extensions: Optional[List[str]] = None,
        mimetypes: Optional[List[str]] = None,
        size_limit: Optional[int] = None,
        size_limit_clear: Optional[bool] = False,
        is_active: Optional[bool] = None,
    ) -> "AttachmentType":
        changes: Dict[str, Any] = {}

        if name is not None and name != self.name:
            changes["name"] = name

        if extensions is not None:
            clean_extensions = clean_list_value(extensions)
            if clean_extensions != self.extensions:
                changes["extensions"] = clean_extensions

        if mimetypes is not None:
            clean_mimetypes = clean_list_value(mimetypes)
            if clean_mimetypes != self.mimetypes:
                changes["mimetypes"] = clean_mimetypes

        if size_limit_clear and size_limit is not None:
            raise ValueError(
                "'size_limit' can't be used together with 'size_limit_clear'"
            )

        if size_limit_clear and self.size_limit is not None:
            changes["size_limit"] = None

        if size_limit is not None:
            changes["size_limit"] = (
                size_limit if size_limit and size_limit > 0 else None
            )

        if is_active is not None and is_active != self.is_active:
            changes["is_active"] = is_active

        if not changes:
            return self

        await AttachmentType.query.filter(id=self.id).update(**changes)

        return self.replace(**changes)

    def delete(self):
        return AttachmentType.query.filter(id=self.id).delete()

    def __str__(self):
        return self.name


def clean_list_value(list_value: Optional[List[str]]) -> List[str]:
    if list_value is None:
        return []

    clean_list = [item.strip().lower() for item in list_value]
    clean_list = list(set(clean_list))
    if "" in clean_list:
        clean_list.remove("")
    clean_list.sort()
    return clean_list
