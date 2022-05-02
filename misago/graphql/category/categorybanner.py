from ariadne_graphql_modules import ObjectType, gql


class CategoryBannerType(ObjectType):
    __schema__ = gql(
        """
        type CategoryBanner {
            align: String!
            background: String!
            height: Int!
            url: String!
        }
        """
    )


class CategoryBannerSizeType(ObjectType):
    __schema__ = gql(
        """
        type CategoryBannerSize {
            full: CategoryBanner!
            half: CategoryBanner!
        }
        """
    )
    __requires__ = [CategoryBannerType]
