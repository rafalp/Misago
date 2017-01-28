Using frontend context
=========================================

When user visits Misago site for first time, his/hers HTTP request is handled by Django which outputs basic version of requested page. If user has JavaScript enabled in the browser, read-only UI is then swapped with React.js components that provide interactivity.

To enable those components easy access to application's state, Misago provides simple "frontend context".


## Exposing Data to JavaScript UI

Misago creates empty dict and makes it available as `frontend_context` attribute on current `HttpRequest` object. This dict is converted into JSON when page is rendered by Django.

This means that as long as initial page wasn't rendered yet, you can preload data in any place that has access to request object, but for performance reasons views and context processors are best to do this.


## Accessing Preloaded Data

The data exposed to React.js by Misago lives in plain JavaScript object available through `misago.get('KEY')`.