from django.conf import settings
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseStorageFinder
from .storage import OptimizedFileStorage


class OptimizedFileFinder(BaseStorageFinder):
    storage = OptimizedFileStorage


class OptimizableFileFinder(object):
    """
    Wraps a finder class in order to exclude files.

    """
    def __init__(self, finder, include_patterns=None):
        self.wrapped = finder
        self.include_patterns = include_patterns or settings.OPTIMIST_FILES

    def list(self, ignore_patterns):
        """
        Delegate the work of this method to the wrapped finder, but filter its
        results.

        """
        for path, storage in self.wrapped.list(ignore_patterns):
            if utils.matches_patterns(path, self.include_patterns):
                yield path, storage

    def __getattr__(self, name):
        """
        Proxy to the wrapped object.

        """
        return getattr(self.wrapped, name)
