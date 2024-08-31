
from cricket.model import TestMethod, TestCase, TestModule

PASS_COLOR = '#28C025'
FAIL_COLOR = '#E32C2E'

PASSSTR = "PASS"
FAILSTR = "FAIL"
INITSTR = "NA"

READ_ERROR = 'read error'

# Display constants for test status
STATUS = {
    TestMethod.STATUS_PASS: {
        'description': u'通过',
        'symbol': u'\u25cf',
        'tag': 'pass',
        'color': PASS_COLOR
    },
    TestMethod.STATUS_SKIP: {
        'description': u'Skipped',
        'symbol': u'S',
        'tag': 'skip',
        'color': '#259EBF'
    },
    TestMethod.STATUS_FAIL: {
        'description': u'失败',
        'symbol': u'F',
        'tag': 'fail',
        'color': FAIL_COLOR
    },
    TestMethod.STATUS_EXPECTED_FAIL: {
        'description': u'Expected\n  failure',
        'symbol': u'X',
        'tag': 'expected',
        'color': '#3C25BF'
    },
    TestMethod.STATUS_UNEXPECTED_SUCCESS: {
        'description': u'Unexpected\n   success',
        'symbol': u'U',
        'tag': 'unexpected',
        'color': '#C82788'
    },
    TestMethod.STATUS_ERROR: {
        'description': 'Error',
        'symbol': u'E',
        'tag': 'error',
        'color': '#E4742C'
    },
}

STATUS_DEFAULT = {
    'description': 'Not\nexecuted',
    'symbol': u'',
    'tag': None,
    'color': '#BFBFBF',
}