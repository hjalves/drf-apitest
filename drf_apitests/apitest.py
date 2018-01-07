from pathlib import Path

import yaml
from django.utils.text import slugify

from drf_apitests.exception import ValidationError


class APITestSuite:
    def __init__(self, top_dir, start_dir, pattern='api/tests/*.yaml'):
        self.top_dir = Path(top_dir)
        self.start_dir = Path(start_dir)
        self.pattern = pattern

    def discover(self):
        path = self.top_dir.joinpath(self.start_dir)
        for file in path.rglob(self.pattern):
            yield APITestDocument.from_yaml(file, self.top_dir)


class APITestDocument:
    def __init__(self, module, filename, name, tests, auth, fixtures, skip):
        self.module = module
        self.filename = filename
        self.name = name
        self.tests = tests
        self.auth = auth
        self.fixtures = fixtures
        self.skip = skip

    @classmethod
    def from_yaml(cls, file, top_dir):
        file = Path(file)
        module = '.'.join(file.parent.relative_to(top_dir).parts)
        with file.open('rt') as f:
            mapping = yaml.load(f)
        mapping = dict(module=module, filename=file.stem, **mapping)
        return cls.validate(mapping)

    @classmethod
    def validate(cls, mapping):
        if 'name' not in mapping:
            raise ValidationError('name is required')
        if 'tests' not in mapping:
            raise ValidationError('tests is required')
        module = mapping['module']
        filename = mapping['filename']
        name = mapping['name']
        tests = mapping['tests']
        auth = mapping.get('auth')
        fixtures = mapping.get('fixtures', [])
        skip = mapping.get('skip', [])
        tests = [APITestCase.validate(test) for test in tests]
        return cls(module, filename, name, tests, auth, fixtures, skip)

    def __repr__(self):
        return f'<APITestDocument: {self.module}.{self.filename}>'


class APITestCase:
    def __init__(self, name, url, url_vars, method, params, skip):
        self.name = name
        self.url = url
        self.url_vars = url_vars
        self.method = method
        self.params = params
        self.skip = skip
        self.slug = slugify(name).replace('-', '_')

        assert self.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'), \
            f"invalid method '{self.method}'"

    @classmethod
    def validate(cls, mapping):
        if 'name' not in mapping:
            raise ValidationError('name is required')
        if 'url' not in mapping:
            raise ValidationError('url is required')
        if 'method' not in mapping:
            raise ValidationError('method is required')
        name = mapping['name']
        url = mapping['url']
        url_vars = mapping.get('url-vars', {})
        # TODO: test url_vars + url
        method = mapping['method']
        params = mapping.get('params', {})
        skip = mapping.get('skip', [])
        # TODO: test types
        return cls(name, url, url_vars, method, params, skip)

    def interpolated_url(self, base_url=''):
        url = base_url + self.url
        for key, value in self.url_vars.items():
            url = url.replace(':' + key, str(value))
        return url
