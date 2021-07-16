## API Basics - Making a Reddit Clone

reddit.com

People can submit links.

People can upvote links.

We call it zappit

### Zappit Models

```bash
$ py -3.9 -m venv .venv39
$ source .venv39/Scripts/activate
$ django-admin startproject zappit
$ mv zappit zappit-project
$ cd zappit-project
$ python manage.py startapp posts
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
sa/sa
```

Create model, 

```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
  post_id = models.BigAutoField(primary_key=True)
  title = models.CharField(max_length=100)
  url = models.URLField()
  poster = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-created_at',)

class Vote(models.Model):
  vote_id = models.BigAutoField(primary_key=True)
  voter = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
  voted_at = models.DateTimeField(auto_now_add=True)
```



Update admin.py

```python
from .models import (
  Post
)

admin.site.register(Post)
```



Add application to INSTALLED_APPS

Migrate



### Django REST Framework (DRF)

https://www.django-rest-framework.org/

https://zappycode.com/api/courses

```bash
$ pip install djangorestframework
```



### Serializers





## Resources

https://www.smashingmagazine.com/2018/01/understanding-using-rest-api/

https://google.github.io/styleguide/shellguide.html

https://google.github.io/styleguide/docguide/style.html

https://developers.google.com/style/code-syntax