from django.db.models import Q

__author__ = 'Alexey Zankevich'


class SugarQ(object):
    """
    S - Django ORM Sugar

    >>> s = SugarQ()
    >>> s.username.get_query_param()
    'username'

    >>> SugarQ().user.username.get_query_param()
    'user__username'

    Typical usage:
    >>> SugarQ().user.username == 'John Smith'
    <Q: (AND: ('user__username__exact', 'John Smith'))>

    """
    def __init__(self, *args, **kwargs):
        self.__parent = kwargs.pop('__parent', None)
        self.__name = kwargs.pop('__name', '')

    def __getattr__(self, item):
        return SugarQ(__name=item, __parent=self)

    def __eq__(self, value):
        """
        >>> SugarQ().user.username == 'John Smith'
        <Q: (AND: ('user__username__exact', 'John Smith'))>
        """
        return self.exact(value)

    def __gt__(self, value):
        """
        >>> SugarQ().user.age > 7
        <Q: (AND: ('user__age__gt', 7))>
        """
        return Q(**{'{}__gt'.format(self.get_query_param()): value})

    def __ge__(self, value):
        """
        >>> SugarQ().user.age >= 7
        <Q: (AND: ('user__age__gte', 7))>
        """
        return Q(**{'{}__gte'.format(self.get_query_param()): value})

    def __lt__(self, value):
        """
        >>> SugarQ().user.age < 7
        <Q: (AND: ('user__age__lt', 7))>
        """
        return Q(**{'{}__lt'.format(self.get_query_param()): value})

    def __le__(self, value):
        """
        >>> SugarQ().user.age <= 7
        <Q: (AND: ('user__age__lte', 7))>
        """
        return Q(**{'{}__lte'.format(self.get_query_param()): value})

    def in_list(self, lst):
        return Q(**{'{}__in'.format(self.get_query_param()): lst})

    def iexact(self, ):
        pass

    def exact(self, value):
        return Q(**{'{}__exact'.format(self.get_query_param()): value})

    def contains(self, s):
        return Q(**{'{}__contains'.format(self.get_query_param()): s})

    def icontains(self, s):
        return Q(**{'{}__icontains'.format(self.get_query_param()): s})

    def get_query_param(self):
        if self.__parent:
            parent_param = self.__parent.get_query_param()
            if parent_param:
                return '__'.join([parent_param, self.__name])
        return self.__name


# creating shortcut
S = SugarQ()

if __name__ == "__main__":
    import doctest
    doctest.testmod()