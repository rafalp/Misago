from bh.services.base_service import BaseService


class CommunityApp(BaseService):
    """
    This is a community-app-web only service.
    It will not be published anywhere and will not be exposed to any other service.
    It is only intended to be used as an interface between the community web app and external BH services.
    """
