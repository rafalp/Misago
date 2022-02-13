from typing import Awaitable, Dict, List, Sequence

from aiodataloader import DataLoader

from ..context import Context
from ..loaders import Loader, batch_load_function
from .get import get_categories_by_id
from .models import Category

batch_load_categories = batch_load_function(get_categories_by_id)


class CategoriesLoader(Loader[Category]):
    context_key = "_categories_loader"

    def get_batch_load_function(self):
        return batch_load_categories


categories_loader = CategoriesLoader()


async def get_categories_children(parents: Sequence[int]) -> List[List[Category]]:
    query = Category.query.filter(parent_id__in=parents).order_by("left").all()
    results: Dict[int, List[Category]] = {parent_id: [] for parent_id in parents}
    for category in await query:
        results[category.parent_id].append(category)

    return [results[parent_id] for parent_id in parents]


class CategoriesChildrenLoader:
    context_key = "_categories_children_loader"

    def setup_context(self, context: Context):
        context[self.context_key] = DataLoader(
            cache=False,
            batch_load_fn=get_categories_children,
        )

    def load(self, context: Context, category_id: int) -> Awaitable[List[Category]]:
        return context[self.context_key].load(category_id)


categories_children_loader = CategoriesChildrenLoader()
