import logging
from pytest import fixture

import numpy as np

from lenskit import util

logging.getLogger('numba').setLevel(logging.INFO)

_log = logging.getLogger('lenskit.tests')


@fixture
def rng():
    return util.rng(42)


@fixture
def legacy_rng():
    return util.rng(42, legacy_rng=True)


@fixture(autouse=True)
def init_rng(request):
    util.init_rng(42)


@fixture(autouse=True)
def log_test(request):
    _log.info('running test %s:%s', request.module.__name__, request.function.__name__)


def pytest_collection_modifyitems(items):
    # add 'slow' to all 'eval' tests
    for item in items:
        evm = item.get_closest_marker('eval')
        slm = item.get_closest_marker('slow')
        if evm is not None and slm is None:
            _log.debug('adding slow mark to %s', item)
            item.add_marker('slow')
