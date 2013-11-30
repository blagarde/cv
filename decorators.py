import functools


def limitable(generator_func):
    '''A decorator that lets you limit the number of results yielded by a generator'''
    def wrapper(*args, **kwargs):
        limit = kwargs.pop('limit', None)
        gen = generator_func(*args, **kwargs)
        return gen if limit is None else (gen.next() for i in xrange(limit))
    return functools.update_wrapper(wrapper, generator_func)
