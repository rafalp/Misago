Search filters
==============

Misago implements small feature that allows forum administrators to define custom search filters that may be used to improve forum searches accuracy without need for developing custom dictionaries.

Consider the scenario in which community is ran for computer game. This game's community will eventually develop jargon of its own that will likely confuse the search engine backed by language's dictionary.

In Misago this situation may be easily solved with custom search filters that post and search queries are passed through before they are sent to search engine. Those filters are simple python functions that take string as only argument, do something with it, and then return changed string back, like this:


```python
def my_search_filter(search):
    """very basic filter that lets search engine understand what MMM stands for"""
    return search.replace('MMM', 'Marines, Medics and Marauders')
```

Misago is made aware of search filters by specifying paths to callables in `MISAGO_POST_SEARCH_FILTERS` setting, like this:

```python
MISAGO_POST_SEARCH_FILTERS = [
    'myforumsearch.filters.my_search_filter',
]
```
