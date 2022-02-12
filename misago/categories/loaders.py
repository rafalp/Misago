from ..loaders import Loader, batch_load_function
from .get import get_categories_by_id
from .models import Category

batch_load_categories = batch_load_function(get_categories_by_id)


class CategoriesLoader(Loader[Category]):
    context_key = "_categories_loader"

    def get_batch_load_function(self):
        return batch_load_categories


categories_loader = CategoriesLoader()
