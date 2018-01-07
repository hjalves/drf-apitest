import json
from functools import partial
from pathlib import Path

from django.test import TestCase
from rest_framework import status


def make_test_class(document, base_url='/api/v1'):
    """Build the unit test class for the given test document.

    :param document: Test document
    :type document: drf_apitests.apitest.APITestDocument
    :param base_url:
    :return:
    """

    def make_test_func(test):
        """Build the unit test method for the given test case.

        :param test: Test case
        :type test: drf_apitests.apitest.APITestCase
        :return:
        """
        full_url = test.interpolated_url(base_url=base_url)

        def log_to_output_file(response):
            dir = Path('_apitest_results') / document.module / document.name
            dir.mkdir(parents=True, exist_ok=True)
            data = (None if response.status_code == 204 else response.json())
            with (dir / f"{test.slug}.json").open('wt') as fp:
                json.dump(dict(response=data, status=response.status_code),
                          fp, indent=4)

        def test_func(self):
            request = getattr(self.client, test.method.lower())
            response = request(full_url, data=test.params, format='json')
            msg = f"Unexpected HTTP response ({response.status_code}): " \
                  f"{response.content}"
            success = (status.HTTP_200_OK, status.HTTP_201_CREATED,
                       status.HTTP_204_NO_CONTENT)
            self.assertIn(response.status_code, success, msg)
            log_to_output_file(response)

        test_func.__name__ = test.slug
        test_func.__doc__ = test.method + ' ' + full_url
        if 'testing' in test.skip:
            test_func.__unittest_skip__ = True
        return test_func

    # Import stuff
    from drf_apitests.client import CustomAPIClient

    # Build class
    class_attrs = {}
    class_attrs['name'] = document.name
    class_attrs['fixtures'] = document.fixtures
    class_attrs['client_class'] = partial(CustomAPIClient, auth=document.auth)
    for test in document.tests:
        class_attrs[test.slug] = make_test_func(test)
    klass = type(document.filename, (TestCase,), class_attrs)
    klass.__module__ = document.module
    if 'testing' in document.skip:
        klass.__unittest_skip__ = True
    return klass
