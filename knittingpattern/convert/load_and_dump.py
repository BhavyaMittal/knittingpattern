"""convinience methods for conversion

Best to use :meth:`decorate_load_and_dump`.

"""
from functools import wraps


def load_and_dump(create_loader, create_dumper, load_and_dump_):
    """:return: a function that has the doc string of
      :paramref:`load_and_dump_`
      additional arguments to this function are passed on to
      :paramref:`load_and_dump_`.

    :param create_loader: a loader, e.g.
      :class:`knittingpattern.Loader.PathLoader`
    :param create_dumper: a dumper, e.g.
      :class:`knittingpattern.Dumper.ContentDumper`
    :param load_and_dump_: a function to call with the loaded content.
      The arguments of both, :paramref:`Loader` and :paramref:`Dumper`
      will be passed to :paramref:`load_and_dump_`.
      Any additional arguments to the return value are also passed to
      :paramref:`load_and_dump_`.
      The return value of :paramref:`load_and_dump_` is passed back to the
      :paramref:`Dumper`.

    """
    @wraps(load_and_dump_)
    def load_and_dump__(*args1, **kw1):
        def load(*args2, **kw2):
            """return the dumper"""
            def dump(*args3, **kw3):
                kw = {}
                kw.update(kw1)
                kw.update(kw2)
                kw.update(kw3)
                return load_and_dump_(*(args1 + args2 + args3), **kw)
            return create_dumper(dump)
        return create_loader(load)
    return load_and_dump__


def decorate_load_and_dump(create_loader, create_dumper):
    """Same as :func:`load_and_dump` but returns a function to enable decorator
    syntax.

    Examples:

    .. code:: Python

        @decorate_load_and_dump(ContentLoader, JSONDumper)
        def convert_from_loader_to_dumper(loaded_stuff, other="arguments"):
            # convert
            return converted_stuff

        @decorate_load_and_dump(PathLoader, lambda dump: ContentDumper(dump,
            encoding=None))
        def convert_from_loader_to_dumper(loaded_stuff, to_file):
            # convert
            to_file.write(converted_stuff)

    """
    return lambda func: load_and_dump(create_loader, create_dumper, func)


__all__ = ["load_and_dump", "decorate_load_and_dump"]
