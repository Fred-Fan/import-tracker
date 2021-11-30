"""
Tests for the lazy_import_errors functionality
"""

# Standard
import os

# Third Party
import pytest

# Local
from test.helpers import reset_sys_modules
import import_tracker

######################## Tests for Direct Invocation of the Context Manager #######################
def test_lazy_import_sad_package(reset_sys_modules):
    """This test makes sure that the ModuleNotFoundError is not raised for an
    unknown module on import, but that it is raised on attribute access.

    This version tests that this is true when imported directly, but wrapped in
    lazy_import_errors.
    """
    with import_tracker.lazy_import_errors():
        import foobarbaz
    with pytest.raises(ModuleNotFoundError):
        foobarbaz.foo()

def test_lazy_import_happy_package_with_sad_optionals(reset_sys_modules):
    """This test uses `numpy` which has several "optional" dependencies in order
    to support backwards compatibility. We need to ensure that these usecases
    are supported such that the downstream libs do not get confused.

    This version tests that the import works when imported directly, but wrapped
    in lazy_import_errors.

    CITE: https://github.com/numpy/numpy/blob/main/numpy/compat/py3k.py#L24
    """
    import pickle
    with import_tracker.lazy_import_errors():
        import numpy
        assert numpy.compat.py3k.pickle is pickle
