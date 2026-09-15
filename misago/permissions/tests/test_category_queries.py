from ..threads import CategoryQueries


class CategoryProxy:
    def __init__(self, id: int):
        self.id = id


def test_category_queries_add_adds_query_str():
    queries = CategoryQueries()
    queries.add("query", CategoryProxy(id=1))

    assert list(queries.items()) == [("query", {1})]


def test_category_queries_add_query_list():
    queries = CategoryQueries()
    queries.add(["a", "b"], CategoryProxy(id=1))

    assert list(queries.items()) == [("a", {1}), ("b", {1})]


def test_category_queries_add_combines_queries():
    queries = CategoryQueries()
    queries.add("see", CategoryProxy(id=1))
    queries.add(["see", "read"], CategoryProxy(id=2))
    queries.add("see", CategoryProxy(id=3))
    queries.add("read", CategoryProxy(id=4))
    queries.add(["see", "read", "like"], CategoryProxy(id=5))

    assert list(queries.items()) == [
        ("see", {1, 2, 3, 5}),
        ("read", {2, 4, 5}),
        ("like", {5}),
    ]


def test_category_queries_tests_false_when_empty():
    queries = CategoryQueries()
    assert not queries


def test_category_queries_tests_true_when_has_contents():
    queries = CategoryQueries()
    queries.add("see", CategoryProxy(id=1))

    assert queries
