#!/usr/bin/env python

"""Setup pylama installation."""

import pathlib

from setuptools import setup


# tokenize requirements file
# Note: according to the specification
# at https://pip.pypa.io/en/stable/reference/requirements-file-format/
# line continuations are processed before comments, however pkg_resources source code
# says otherwise:
# def parse_requirements(strs: _NestedStr) -> map[Requirement]:
#     return map(Requirement, join_continuation(map(drop_comment, yield_lines(strs))))
# Here we follow the actual implementation.
def join_continuation(lines):
    lines = iter(lines)
    for item in lines:
        while item.endswith('\\'):
            try:
                item = item[:-2].strip() + next(lines)
            except StopIteration:
                return
        yield item


def drop_comments(lines):
    for item in lines:
        yield item.partition(' #')[0]


def drop_whites(lines):
    for item in lines:
        stripped = item.strip()
        if stripped:
            yield stripped


def requirements_from_file(path: str) -> 'list[str]':
    with pathlib.Path(path).open(encoding='utf-8') as f:
        return list(drop_whites(join_continuation(drop_comments(f))))


OPTIONAL_LINTERS = ['pylint', 'eradicate', 'radon', 'mypy', 'vulture']


setup(
    install_requires=requirements_from_file('requirements/requirements.txt'),
    extras_require=dict(
        tests=requirements_from_file('requirements/requirements-tests.txt'),
        all=OPTIONAL_LINTERS, **{linter: [linter] for linter in OPTIONAL_LINTERS},
        toml='tomli>=1.2.3; python_version < "3.11"',
    ),
)
