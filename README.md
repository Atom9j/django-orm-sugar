# Django ORM Sugar [![Build Status](https://travis-ci.org/Nepherhotep/django-orm-sugar.svg?branch=q_object_integration)](https://travis-ci.org/Nepherhotep/django-orm-sugar)
Sugar library to simplify Django querying

## Overview 

Django ORM Sugar

The updated helper replaces calls like
```python     
SomeModel.objects.filter(user__profile__common_bucket__seq_count__gte=7)
```
    
With more pythonic syntax
```python
from django_orm_sugar import Q

SomeModel.objects.filter(Q.user.profile.common_bucket.seq_count >= 7)
```

It gets easy to follow DRY principles when working with long query paths
```python
from django_orm_sugar import Q

# saving reference for QFactory
seq_count = Q.user.profile.common_bucket.seq_count

# using it multiple times - in filter and order_by calls
SomeModel.objects.filter(seq_count >= 7).order_by(seq_count.get_path())
```

It is still possible to create Q objects in the old style way:
```python
q = Q(user__profile__common_bucket__seq_count=1)
```

## Queries
General comparison actions generate related Q objects:  
```python
>>> Q.user.username == 'Bender Rodriguez'
Q(user__username='Bender Rodriguez')

>>> Q.user.age > 7
Q(user__age__gt=7)

>>> Q.user.age >= 7
Q(user__age__gte=7)

>>> Q.user.age < 7
Q(user__age__lt=7)

>>> Q.user.age <= 7
Q(user__age__lte=7)
```

Filter by null (or not-null) fields
```python
>>> Q.user.favorite_movie.is_null()
Q(user__favorite_movie__isnull=True)
```

Filter by fields matching a given list
```python
>>> Q.user.id.in_list([1, 2, 3])
Q(user__id__in=[1, 2, 3])
```
   
Filter by fields in range
```python
>>> Q.user.id.in_range(7, 10)
Q(user__id__lte=7) & Q(user__id__gte=10)
```
    
Common Django filter shortcuts
```python
>>> Q.user.username.iexact('Bender Rodriguez')
Q(user__username__iexact='Bender Rodriguez')

>>> Q.user.username.exact('Bender Rodriguez')
Q(user__username__exact='Bender Rodriguez')

>>> Q.user.username.contains('Rodriguez')
Q(user__username__contains='Rodriguez')

>>> Q.user.username.icontains('Rodriguez')
Q(user__username__icontains='Rodriguez')
```

Get query path - useful for order_by, select_related and other calls,
which expect query path as string
```python
>>> Q.user.username.get_path()
'user__username'
```

## Extending

You can extend helper with your own methods. Let's say you need to create
in_exc_range() helper, which will perform exclusive range filtering.
  
Step 1. Extend QFactory class:
```python
from django_orm_sugar import QFactory

class RangedQueryHelper(QFactory):
    pass
```

Step 2. Create Helper Method
```python
class RangedQueryHelper(QFactory):
    def in_exc_range(self, min_value, max_value):
        """
        Unlike existing in_range method, filtering will be performed
        excluding initial values. In other words - we will use "<" and ">"
        comparison instead of "<=" and ">="
        """
        return (self < min_value) & (self > max_value)
```

Step 3. Initialize Helper Instance
```python
    Q = RangedQueryHelper()  # can be done whether in function or module level
```

Step 4. Now you can use it in your code
```python
>>> Q.registration_date.in_exc_range(from_date, to_date)
Q(registration_date__gt=from_date) & Q(registration_date__lt=to_date)
```
