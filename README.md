# ModelViewSet Implementation

**Please note:** read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md)
before start.

In this task, you should implement:
- the `AuthorSerializer` serializer for the `Author` model in `serializers.py`;
- the `AuthorViewSet` viewset in `views.py`.

The `Author` model has the following fields:
- first_name (with the `max_length` of 64);
- last_name (with the `max_length` of 64);
- pseudonym (with the `max_length` of 64, can be null);
- age (integer field);
- retired (boolean field).

**Please note:** you should also modify `author.urls.py` to make things work.
