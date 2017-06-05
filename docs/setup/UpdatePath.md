Update path
===========

Some versions of Misago contain migrations for deprecated features. 

## 0.6 Alphas to 0.6

### Some database indexes have changed

Misago 0.6 final release contains special migrations that replace old database indexes with new ones using custom `PgPartialIndex` index class that uses custom index types feature that was introduced in the Django 1.11.


## 0.6 to 0.7

### `misago.datamover` has been removed

`misago.datamover` entry in your `settings.py` `INSTALLED_APPS` setting is an error in Misago 0.7 and should be removed. Likewise the `url(r'^', include('misago.datamover.urls'))` entry in your `urls.py` will also error and has to be removed.

If you have updated to Misago 0.6 from Misago 0.5 and you looking to preserve redirects from old links after update to 0.7, please use the [Misago 0.5 Redirects](https://github.com/rafalp/Misago-05-Redirects) app.


### `CreatePartialIndex` and `CreatePartialCompositeIndex` migration utilities have been removed

0.7 release finalizes deprecation of previous implementation of custom indexes via removal of old migration utilities as well as their migrations. Attempting the update from any of the 0.6's alphas to 0.7 and skipping the 0.6 final release on the way will lead to your database containing both old and new indexes which may be source of errors in future migrations.