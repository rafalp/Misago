from typing import Awaitable, List, Optional, Union

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...categories.loaders import categories_children_loader, categories_loader
from ...categories.models import Category
from ..scalars import GenericScalar
from .categorybanner import CategoryBannerSizeType


class CategoryType(ObjectType):
    __schema__ = gql(
        """
        type Category {
            id: ID!
            parent: Category
            children: [Category!]!
            depth: Int!
            name: String!
            slug: String!
            color: String
            icon: String
            banner: CategoryBannerSize
            threads: Int!
            posts: Int!
            isClosed: Boolean!
            extra: Generic!
        }
        """
    )
    __aliases__ = {
        "isClosed": "is_closed",
    }
    __requires__ = [GenericScalar, CategoryBannerSizeType]

    @staticmethod
    def resolve_parent(
        category: Category, info: GraphQLResolveInfo
    ) -> Optional[Awaitable[Optional[Category]]]:
        if category.parent_id:
            return categories_loader.load(info.context, category.parent_id)
        return None

    @staticmethod
    def resolve_children(
        category: Category, info: GraphQLResolveInfo
    ) -> Union[Awaitable[List[Category]], List[Category]]:
        if category.has_children():
            return categories_children_loader.load(info.context, category.id)

        return []

    @staticmethod
    def resolve_banner(category: Category, info: GraphQLResolveInfo) -> dict:
        return {
            "full": {
                "align": "center",
                "background": "#2c3e50",
                "height": 100,
                "url": "http://placekitten.com/1280/200/",
            },
            "half": {
                "align": "center",
                "background": "#2c3e50",
                "height": 100,
                "url": "http://placekitten.com/768/200/",
            },
        }

    @staticmethod
    def resolve_threads(category: Category, info: GraphQLResolveInfo) -> int:
        categories_index = info.context["categories"]
        return categories_index[category.id].threads

    @staticmethod
    def resolve_posts(category: Category, info: GraphQLResolveInfo) -> int:
        categories_index = info.context["categories"]
        return categories_index[category.id].posts

    @staticmethod
    def resolve_is_closed(category: Category, info: GraphQLResolveInfo) -> bool:
        categories_index = info.context["categories"]
        return categories_index[category.id].is_closed

    @staticmethod
    def resolve_extra(category: Category, info: GraphQLResolveInfo) -> dict:
        return {}


class AdminCategoryType(CategoryType):
    @staticmethod
    def resolve_threads(category: Category, info: GraphQLResolveInfo) -> int:
        categories_index = info.context["categories"]
        return category.threads

    @staticmethod
    def resolve_posts(category: Category, info: GraphQLResolveInfo) -> int:
        return category.posts

    @staticmethod
    def resolve_is_closed(category: Category, info: GraphQLResolveInfo) -> bool:
        return category.is_closed
