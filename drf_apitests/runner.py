from unittest import TestLoader

from django.test.runner import DiscoverRunner

from drf_apitests.apitest import APITestSuite
from drf_apitests.metaclass import make_test_class


class CustomTestLoader(TestLoader):
    def discover(self, start_dir, pattern='api/tests/*.yaml',
                 top_level_dir=None):
        test_suite = APITestSuite(top_level_dir, start_dir, pattern)

        for doc in test_suite.discover():
            klass = make_test_class(doc)
            yield self.suiteClass(klass(test.slug) for test in doc.tests)


class APITestRunner(DiscoverRunner):
    test_loader = CustomTestLoader()

    @classmethod
    def add_arguments(cls, parser):
        # TODO: other arguments
        default_pattern = 'api/tests/*.yaml'
        parser.add_argument(
            '-p', '--pattern', action='store', dest='pattern',
            default=default_pattern,
            help='The test matching pattern. Defaults to: ' + default_pattern,
        )
