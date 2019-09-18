#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0330
"""Storage backend for keyring and obfuscated environment variables.

Link:
    https://github.com/jaraco/keyring

"""
import base64
import os
import sys

import keyring

if sys.version_info[:2] >= (3, 5):
    # Python 3.5
    import importlib.util
else:
    # Python 2 code
    import imp


class Storage:
    KEYRING_ENV = "OS-ENV"
    KEYRING_USER = "JSON"

    SESSION_STORAGE_VARIABLE = "OS_ENV_STORAGE"

    STORAGE_BACKEND_KEYRING = 0
    STORAGE_BACKEND_SESSION = 1

    active_storage_backend = None

    def __init__(self, backend=None):
        """Constructor: run's backend check and can overwrite backend settings."""
        if (backend is not None) and (
            backend == self.STORAGE_BACKEND_KEYRING
            or backend == self.STORAGE_BACKEND_SESSION
        ):
            # check if backend is valid
            self.active_storage_backend = backend
        else:
            self.run_self_check()

    def run_self_check(self):
        """Check if keyring is working and if not then switch backend."""
        self.active_storage_backend = self.STORAGE_BACKEND_SESSION

        # check for keyring module
        if sys.version_info[:2] >= (3, 5):
            # Python 3.5
            import_result = importlib.util.find_spec("keyring")
        else:
            # Python 2 code
            import_result = imp.find_module("keyring")

        if import_result is not None:

            # check to store data to keyring
            try:
                keyring.set_password(
                    "KEYRING_TEST", "SYSTEM", "QWERTZUIOASDFGHJKLYXCVBNM"
                )
            except:
                return

            # check to get data from keyring
            try:
                password = keyring.get_password("KEYRING_TEST", "SYSTEM")
                if password != "QWERTZUIOASDFGHJKLYXCVBNM":
                    raise Exception("Keyring do not work properly. Abort!")
            except:
                return

            self.active_storage_backend = self.STORAGE_BACKEND_KEYRING

    def set_data(self, data):
        """Public data setter."""
        if self.active_storage_backend == self.STORAGE_BACKEND_KEYRING:
            self._set_data_to_keyring(data)
        elif self.active_storage_backend == self.STORAGE_BACKEND_SESSION:
            output = self._set_data_to_session(data)
            print(output)
        else:
            print(
                "Given storage backend unsopported: {0}".format(
                    self.active_storage_backend
                )
            )

    def get_data(self):
        """Public data getter."""
        if self.active_storage_backend == self.STORAGE_BACKEND_KEYRING:
            return self._get_data_from_keyring()
        elif self.active_storage_backend == self.STORAGE_BACKEND_SESSION:
            return self._get_data_from_session()
        else:
            print(
                "Given storage backend unsopported: {0}".format(
                    self.active_storage_backend
                )
            )
            return None

    def del_data(self):
        """Public data delete."""
        if self.active_storage_backend == self.STORAGE_BACKEND_KEYRING:
            self._del_data_from_keyring()
        elif self.active_storage_backend == self.STORAGE_BACKEND_SESSION:
            self._del_data_from_session()
        else:
            print(
                "Given storage backend unsopported: {0}".format(
                    self.active_storage_backend
                )
            )

    def _set_data_to_keyring(self, data):
        # here or inside controller: json_data.decode("utf-8")

        # save to keyring
        try:
            keyring.set_password(self.KEYRING_ENV, self.KEYRING_USER, data)
        except NameError:
            print("NameError: Keyring unkown...")
        except keyring.errors.PasswordSetError:
            print("Couldn't save environments to keyring...")
        except RuntimeError:
            print("No keyring backend available.")
        except:
            print("Unexpected error: ", sys.exc_info()[0])

    def _get_data_from_keyring(self):
        try:
            data = keyring.get_password(self.KEYRING_ENV, self.KEYRING_USER)
        except RuntimeError:
            print("No keyring backend available.")
            return None
        return data

    def _del_data_from_keyring(self):
        try:
            keyring.delete_password(self.KEYRING_ENV, self.KEYRING_USER)
        except keyring.errors.PasswordDeleteError:
            pass
        except RuntimeError:
            print("No keyring backend available.")
        except:
            print("Keyring: Error while deleting password.")

    def _set_data_to_session(self, data):
        # bdata = data.encode('base64')
        bdata = base64.b64encode(data.encode("utf-8"))

        os.environ[Storage.SESSION_STORAGE_VARIABLE] = bdata.decode("utf-8")

        return "export {name}={value}".format(
            name=self.SESSION_STORAGE_VARIABLE, value=bdata.decode("utf-8")
        )

    def _get_data_from_session(self):
        try:
            bdata = os.environ[self.SESSION_STORAGE_VARIABLE]
        except KeyError:
            print("Please load session before using: $ os-env -r <encoded-file>")

        data = base64.b64decode(bdata.encode("utf-8"))
        return data.decode("utf-8")

    def _del_data_from_session(self):
        try:
            del os.environ[self.SESSION_STORAGE_VARIABLE]
            return "unset {name}".format(name=self.SESSION_STORAGE_VARIABLE)
        except KeyError:
            return None
