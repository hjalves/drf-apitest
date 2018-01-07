
from drf_apitests.apitest import APITestCase

def test_apitestcase_validate():
    mapping = {'name': 'test case',
               'url': 'http://localhost:8080/path/to/:var',
               'url-vars': {'var': 'wololo'},
               'method': 'GET',
               'params': {'q': 'query'}}
    testcase = APITestCase.validate(mapping)
    assert testcase.name == 'test case'
    assert testcase.url == 'http://localhost:8080/path/to/:var'
    assert testcase.url_vars == {'var': 'wololo'}
    assert testcase.method == 'GET'
    assert testcase.params == {'q': 'query'}

