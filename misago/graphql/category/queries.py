from typing import Awaitable, List, Optional

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...categories.get import get_all_categories, get_root_categories
from ...categories.loaders import categories_loader
from ...categories.models import Category
from ..args import clean_id_arg, handle_invalid_args
from ..adminqueries import AdminQueries
from .category import AdminCategoryType, CategoryType


class CategoryQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            categories: [Category!]!
            category(id: ID!): Category
        }
        """
    )
    __requires__ = [CategoryType]

    @staticmethod
    @handle_invalid_args
    def resolve_category(
        _,
        info: GraphQLResolveInfo,
        *,
        id: str,  # pylint: disable=redefined-builtin
    ) -> Awaitable[Optional[Category]]:
        category_id = clean_id_arg(id)
        return categories_loader.load(info.context, category_id)

    @staticmethod
    def resolve_categories(*_) -> Awaitable[List[Category]]:
        return get_root_categories()


class AdminCategoryQueries(AdminQueries):
    __schema__ = gql(
        """
        type Query {
            categories: [Category!]
            category(id: ID!): Category
        }
        """
    )
    __requires__ = [AdminCategoryType]

    @staticmethod
    @handle_invalid_args
    def resolve_category(
        _,
        info: GraphQLResolveInfo,
        *,
        id: str,  # pylint: disable=redefined-builtin
    ) -> Awaitable[Optional[Category]]:
        category_id = clean_id_arg(id)
        return categories_loader.load(info.context, category_id)

    @staticmethod
    def resolve_categories(*_) -> Awaitable[List[Category]]:
        return get_all_categories()
