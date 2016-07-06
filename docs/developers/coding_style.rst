============================
Coding Style and Conventions
============================

When writing Python code for Misago, please familiarize yourself with and follow those documents:

1. `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_
2. `Django Coding Style and Conventions <https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/>`_

Those documents should give you solid knowledge of coding style and conventions that are followed by Python and Django programmers when writing code.

In addition to those guidelines, Misago defines set of additional convetions and good practices that will help you write better and easier code.


.. note::
   Originally Misago was writen with 79 character line limit in mind, but recently this convention was dropped for sake of Django's 119 characters line limit. 

.. note::
   Misago comes with ".pylintrc" file that contains configuration for pylint tool used to lint Misago's codebase.


Models
======

Fields Order
------------

When declaring model's database fields, start with taxonomical foreign keys followed by fields that make this model identifiable to humans. Order of remaining fileds is completely up to you.

Thread model is great example of this convention. Thread is part of taxonomy (Forum), so first field defined is foreign key to Forum model. This is followed by two fields that humans will use to recognise this model: "title" that will be displayed in UI and "slug" that will be included in links to this thread. After those Thread model defines additional fields.

When declaring model database fields, make sure they are grouped together based on their purpose. Most common example is storage of user name and slug in addition to foreign key to User model. In such case, make sure both "poster" field as well as "poster_name", "poster_slug" and "poster_ip" fields are grouped together.


Avoid Unmeaningful Names
------------------------

Whenever possible avoid naming fields representing relation to "User" model "user". Preffer more descriptive names like "poster", "last_editor", or "giver".

For same reason avoid using "date" or "ip" as field names. Use more descriptive "posted_on" or "poster_ip" instead.


True/False Fields
-----------------

For extra clarity prefix fields representing true/false states of model with "is". "is_deleted" is better than "deleted".


Serializers
===========

Defining serializers
--------------------

Model's default serializer should be named after its model, but with "Serializer" suffix, ergo serializer for "Thread" model should be named "ThreadSerializer". Default serializer should be only serializer defining serialization methods.

In case that model has more than one serializer, all serializers should inherit from default one and be named in a way describing it usage. For example serializer for "User" model used to serialize post's author should be named "PostPosterSerializer". This serializer should only define "Meta" class with "model" and "fields" attributes, inheriting serialization behaviour form default serializer.


Fields Order
------------

Order of fields should correspond directly to order of fields on model that serializer handles.

If serializer defines non-model fields, those should be specified last and separated from model's fields with empty line, ergo::

    fields = (
        'id',
        'user',
        'title',

        'acl', # annotation set on model by view
        'something_extra', # dynamic atribute coming from "SerializerMethodField"
    )


URLs
----

Serializers may define two special fields used for serialization of url's, "url" and "api". The first one should be string containing serialized model's "get_absolute_url" or list urls of interest for UI rendering serialized model, like::

    'url': {
        'absolute': obj.get_absolute_url(),
        'first_unread': obj.get_first_unread_url(),
        'last_post': obj.get_last_post_url(),
    }

Likewise the "api" key should contain the url to item api endpoint (eg. "/api/threads/132/") or list of avaiable endpoints::

    'api': {
        'index': reverse('misago:api:threads', kwargs={'pk': obj.pk}),
        'read': reverse('misago:api:thread-read', kwargs={'pk': obj.pk}),
        'move': reverse('misago:api:thread-move', kwargs={'pk': obj.pk}),
    }

Those keys should live at the end of the fields list and be separated from other fields with blank line::

    fields = (
        'id',
        'user',
        'title',

        'acl', # annotation set on model by view
        'something_extra', # dynamic atribute coming from "SerializerMethodField"

        'api',
        'url',
    )


Nested results
--------------

Nested results should be included in view or viewset, as part of creding dict of serialized data for "Response" object::

    data = UserSerializer(user).data
    data['post_set'] = UserPostSerializer(posts, many=True).data
    return Response(data)

The added key should be model's "related_name" in respect of model it annotates (defautly its "modelname_set").