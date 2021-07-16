## API Basics - Making a Reddit Clone

reddit.com

People can submit links.

People can upvote links.

We call it zappit

### 1. Zappit Models

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



### 2. Django REST Framework (DRF)

https://www.django-rest-framework.org/

https://zappycode.com/api/courses

```bash
$ pip install djangorestframework
```



### 3. Serializers

Create `posts/serializer.py`:

```python
from rest_framework import serializers
from .models import (
  Post,
)

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ('post_id', 'title', 'url', 'poster', 'created_at')
```



Create a view:

```python
from django.shortcuts import render
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class PostList(generics.ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
```

Create `posts/urls.py`

```python
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
  path('posts/', views.PostList.as_view(), name='posts-data'),
]
```



Register posts urls into project's urls:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('posts.urls', namespace='posts')),
]
```



Explore http://localhost:8000/api/posts/

### 4. Adding Posts to the Database

Make sure models are registered in `posts/admin.py`:

```python
from django.contrib import admin
from .models import (
  Post,
  Vote,
)

admin.site.register(Post)
admin.site.register(Vote)
```

Open admin: http://localhost:8000/admin/

Add posts from admin interface.

### 5. Creating Posts via the API

Change the PostList view to ListCreateAPIView:

```python
class PostList(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
```

Now you can post to the same url to create posts.

Tyr it. See https://www.restapitutorial.com/httpstatuscodes.html for HTTP status codes.

Make poster read only field - modify `posts/serializers.py`:

```python
from rest_framework import serializers
from .models import (
  Post,
)

class PostSerializer(serializers.ModelSerializer):
  poster = serializers.ReadOnlyField(source='poster.username')
  poster_id = serializers.ReadOnlyField(source='poster.id')
  class Meta:
    model = Post
    fields = ('post_id', 'title', 'url', 'poster', 'poster_id', 'created_at')
```

also add a method to the `PostList` view:

```python
  def perform_create(self, serializer):
    serializer.save(poster=self.request.user)
```



Adjust authorization - modify `posts/views.py`:

```python
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def perform_create(self, serializer):
    serializer.save(poster=self.request.user)

```





## Swagger Interface

See https://igeorgiev.eu/python/misc/python-django-rest-framework-opeanapi-swagger-documentation/

``` bash
$ python manage.py startapp api_docs
$ pip install pyyaml uritemplate
```

Add setting to project's `settings.py`:

```python
API_TITLE = 'Zappit API'
```

Create `api_docs/urls.py`:

```python
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework import renderers
from django.conf import settings

urlpatterns = [
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema-yaml'}
    ), name='swagger-ui'),
    path('openapi.yaml', get_schema_view(
            title=settings.API_TITLE,
            renderer_classes=[renderers.OpenAPIRenderer]
        ), name='openapi-schema-yaml'),
    path('openapi.json', get_schema_view(
            title=settings.API_TITLE,
            renderer_classes = [renderers.JSONOpenAPIRenderer],
        ), name='openapi-schema-json'),
]
```

create `api_docs/templates/swagger-ui.html`:

```django
<!DOCTYPE html>
<html>
  <head>
    <title>Swagger</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
    const ui = SwaggerUIBundle({
        url: "{% url schema_url %}",
        dom_id: '#swagger-ui',
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        requestInterceptor: (request) => {
          request.headers['X-CSRFToken'] = "{{ csrf_token }}"
          return request;
        }
      })
    </script>
  </body>
</html>
```

Register `api_docs` app in `INSTALLED_APPS` in `settings.py`

Add `api_docs` urls to project urls:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('', include('api_docs.urls')),
    # ...
]
```



## Resources

https://www.smashingmagazine.com/2018/01/understanding-using-rest-api/

https://google.github.io/styleguide/shellguide.html

https://google.github.io/styleguide/docguide/style.html

https://developers.google.com/style/code-syntax