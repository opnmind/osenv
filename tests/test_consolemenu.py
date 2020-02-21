#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0330
import pytest
import unittest
import mock
import os
import sys
from mock import Mock
from unittest.mock import patch

from lib.osenv_controller import OSEnvController

class TestConsolemenu(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('builtins.input', side_effect=[
        1,
        "UNITTEST",
        "unittest_OS_USER_DOMAIN_NAME",
        "unittest_OS_USERNAME",
        "unittest_OS_TENANT_NAME",
        "unittest_OS_PROJECT_NAME",
        "unittest_OS_AUTH_URL",
        "unittest_S3_ACCESS_KEY_ID",
        "unittest_S3_HOSTNAME",
        3,
        4
        ])
    @patch('getpass.getpass', side_effect=[
        "unittest_OS_PASSWORD",
        "unittest_S3_SECRET_ACCESS_KEY"
        ])
    def test_add_and_write_dataset(self, mock_input, mock_getpass):        
        stdout = mock.MagicMock()
        arguments = Mock()  
        arguments.write = "./unittest.ostackrc.enc"

        result = OSEnvController.action_write(arguments)
        self.assertEqual(os.path.exists(arguments.write), 1)
        st = os.stat(arguments.write)
        self.assertGreaterEqual(oct(st.st_mode), "0o100600")
        self.assertTrue(result)
        os.remove(arguments.write)
            
        
if __name__ == '__main__':
    unittest.main()