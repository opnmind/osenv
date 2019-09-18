#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0330
"""Common test functionality for storage backend."""
from contextlib import contextmanager
from io import StringIO
import os
import sys
import unittest
import warnings

import keyring
from lib.storage import Storage


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestStorageSession(unittest.TestCase):
    data = (
        "https://python-reference.readthedocs.io/en/latest/docs/statements/assert.html"
    )

    def setUp(self):
        self.storage = Storage(backend=Storage.STORAGE_BACKEND_SESSION)
        self.storage.del_data()
        self.storage.set_data(self.data)

    def tearDown(self):
        self.storage.del_data()

    def test_get_data_session(self):
        rdata = self.storage.get_data()
        self.assertEqual(self.data, rdata)

    def test_del_data_session(self):
        with captured_output() as (del_out, del_err):
            self.storage.del_data

        self.assertIn(del_out.getvalue().strip(), "unset")

        try:
            rdata = os.environ[Storage.SESSION_STORAGE_VARIABLE]
            self.assertIsNot(self.data, rdata)
        except KeyError:
            self.assertIsNone(None)


"""Python 2 compat."""
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

if "ResourceWarning" not in vars(builtins):

    class ResourceWarning(Warning):
        pass

try:
    keyring.set_password("TESTSYS", "BACKEND_TEST", "OK")
    password = keyring.get_password("TESTSYS", "BACKEND_TEST")
    if password is not "OK":
        raise RuntimeError
    keyring.delete_password("TESTSYS", "BACKEND_TEST")
    keyring_backend_available = True
except RuntimeError:
    keyring_backend_available = False


@unittest.skipIf(
    keyring_backend_available is False, "No keyring backend not available."
)
@unittest.skipIf(sys.version_info[:2] <= (2, 7), "Keyring does not support python 2.7.")
class TestStorageKeyring(unittest.TestCase):
    data = (
        "https://python-reference.readthedocs.io/en/latest/docs/statements/assert.html"
    )

    def setUp(self):
        """Surpress RessourceWarnings.

        Link:
            https://github.com/jaraco/keyring/issues/380&https://github.com/jaraco/keyring/pull/381
        """
        with warnings.catch_warnings():
            warnings.filterwarnings(
                action="ignore", message="unclosed", category=ResourceWarning
            )

            self.storage = Storage(backend=Storage.STORAGE_BACKEND_KEYRING)
            self.storage.del_data()
            self.storage.set_data(self.data)

    def tearDown(self):
        self.storage.del_data()

    def test_get_data_keyring(self):
        rdata = self.storage.get_data()
        self.assertEqual(self.data, rdata)

    def test_del_data_keyring(self):
        self.storage.del_data()
        self.assertIsNone(self.storage.get_data())


class TestStorage(unittest.TestCase):
    def test_self_check_backend(self):
        """Surpress RessourceWarnings.

        Link:
            https://github.com/jaraco/keyring/issues/380&https://github.com/jaraco/keyring/pull/381
        """
        with warnings.catch_warnings():
            warnings.filterwarnings(
                action="ignore", message="unclosed", category=ResourceWarning
            )

            status = False
            self.storage = Storage()

            if (
                self.storage.active_storage_backend
                == self.storage.STORAGE_BACKEND_KEYRING
                or self.storage.active_storage_backend
                == self.storage.STORAGE_BACKEND_SESSION
            ):
                status = True

            self.assertTrue(status)
