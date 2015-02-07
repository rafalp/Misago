=====================================
Preloading Data for Ember.js Frontend
=====================================

When user visits Misago site for first time, his/hers HTTP request is handled by Django which outputs simple version of requested page. If user has JavaScript enabled in browser, full version of page is then ran by Ember.js.

To keep this process as fast as possible, Misago already includes ("preloads") some of data within initial response. This data is assigned to global ``MisagoData`` object and accessed via ``MisagoPreloadStore`` helper.


Preloading Custom Data
----------------------

Misago creates empty dict and makes it available as ``preloaded_ember_data`` attribute on ``HttpRequest`` object. This dict is converted into JSON when initial page is rendered by Django.

This means that as long as initial page wasn't rendered yet, you can preload data in any place that has access to request object.


Accessing Preloaded Data
------------------------

Misago provides utility object defined within ``misago/utils/preloadstore`` module that provides simple API for accessing keys defined in ``MisagoData``::


    // some .js module that wants to access preloaded data
    import MisagoPreloadStore from 'misago/utils/preloadstore';

    // see if required key is defined
    if (MisagoPreloadStore.has('thread')) {
        // get key value from store
        var preloadedThread = MisagoPreloadStore.get('thread');
    }

    // or use default if key isn't set
    var somethingElse = MisagoPreloadStore.get('nonexistantKey', {'default': 'Value'})

    // pop value so future code doesn't access it
    var preloadedThread = MisagoPreloadStore.pop('thread');
    console.log(MisagoPreloadStore.get('thread')); // prints "undefined" in console

    // finally set values in store (useful for testing, but terrible for global state)
    MisagoPreloadStore.get('fakeValue', {'mock': 'Value'})
