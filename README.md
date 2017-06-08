# django-simditor
django simditor

Installation
------------

    pip install django-simditor

**Add `simditor` to your `INSTALLED_APPS` setting.**

```python
from django.db import models
from simditor.fields import RichTextField


class Post(models.Model):
    content = RichTextField()
```


![](resources/demo.png)
