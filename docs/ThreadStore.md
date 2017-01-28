Thread store
============

Thread store is simple memory-based store that some Misago features use to maintain and pass around state for request duration.

Thread store lives in `misago.core.threadstore` and offers subset of standard cache API known from Django


##### Note

Never use thread store for messaging between parts of your code. Usage of this feature for this is considered bad practice that leads to code with flow that is hard to understand.


## `get(key, default=None)`

Get value for key from thread store or fallback value if key is undefined:

```python
from misago.core import threadstore

threadstore.get('peach')
# returns None

threadstore.get('peach', 'no peach!')
# returns "no peach!"
```


`get()` never raises an exception for non-existant value which is why you should avoid storing `None` values and use custom default values to spot non-existant keys.


## `set(key, value)`

Set value for a key on thread store. This value will then be stored until you overwrite it with new value, thread is killed, `misago.core.middleware.ThreadStoreMiddleware` `process_response` method is called, or you explictly call `clear()` function, clearing thread store.


## `clear()`

Delete all values from thread store. This function is automatically called by `ThreadStoreMiddleware` to make sure contents of thread store won't have effect on next request.