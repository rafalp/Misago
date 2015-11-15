=========================================
Preloading Data for Mithril.js Components
=========================================

When user visits Misago site for first time, his/hers HTTP request is handled by Django which outputs basic version of requested page. If user has JavaScript enabled in browser, blank spaces are then filled by the Mithril.js components.

To enable those components easy access to application's state, Misago provides simple "frontend context".


Exposing Data to Mithril.js
---------------------------

Misago creates empty dict and makes it available as ``frontend_context`` attribute on current ``HttpRequest`` object. This dict is converted into JSON when initial page is rendered by Django.

This means that as long as initial page wasn't rendered yet, you can preload data in any place that has access to request object, but for performance reasons views and context processors are prefereable place to do this.


Accessing Preloaded Data
------------------------

The data exposed to Mithril.js by Misago lives in plain JavaScript object available as ``context`` attribute on services containter instance.
