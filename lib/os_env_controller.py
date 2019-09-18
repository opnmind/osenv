#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0330
import json
import os
import stat
import sys

from consolemenu import SelectionMenu
from lib.file_encryption import FileEncryption
from lib.storage import Storage
from lib.tenant import Tenant


class OSEnvController:

    FILE_PERMISSION = "0o100600"

    @staticmethod
    def action_environment(args):
        """Load ENV from keyrings to active SESSION."""
        storage = Storage()
        json_data = storage.get_data()
        data = json.loads(json_data)

        # print("List of available environments:\n")
        if data:
            for i, osenv in data.items():
                env = next(iter(osenv)).split("_")[0]

                if env == args.environment:
                    tenant = Tenant(env)
                    tenant.import_data(data=osenv, prefix=env)
                    print(tenant.export_ostackrc())
        else:
            print("No environments loaded...")

    @staticmethod
    def action_list():
        """Show available ENV's from keyring."""
        storage = Storage()
        if (
            storage.active_storage_backend == storage.STORAGE_BACKEND_SESSION
            and os.environ.get(Storage.SESSION_STORAGE_VARIABLE) is None
        ):
            print('Active session not found. Please load with "osenv -r".')
            sys.exit(1)

        storage = Storage()
        json_data = storage.get_data()
        data = json.loads(json_data)

        # print("List of available environments:\n")
        if data:
            for i, osenv in data.items():
                env = next(iter(osenv)).split("_")[0]
                print("{0}".format(env))
        else:
            print("No environments loaded...")

    @staticmethod
    def action_clean():
        """Clean up the active SESSION."""
        """
        del os.environ['OS_USER_DOMAIN_NAME']
        del os.environ['OS_USERNAME']
        del os.environ['OS_PASSWORD']
        del os.environ['OS_TENANT_NAME']
        del os.environ['OS_PROJECT_NAME']
        del os.environ['OS_AUTH_URL']
        del os.environ['S3_ACCESS_KEY_ID']
        del os.environ['S3_SECRET_ACCESS_KEY']
        del os.environ['S3_HOSTNAME']
        del os.environ['NOVA_ENDPOINT_TYPE']
        del os.environ['OS_ENDPOINT_TYPE']
        del os.environ['CINDER_ENDPOINT_TYPE']
        del os.environ['OS_VOLUME_API_VERSION']
        del os.environ['OS_IDENTITY_API_VERSION']
        del os.environ['OS_IMAGE_API_VERSION']
        """
        print("unset {0}".format(Storage.SESSION_STORAGE_VARIABLE))
        print("unset OS_USER_DOMAIN_NAME")
        print("unset OS_USERNAME")
        print("unset OS_PASSWORD")
        print("unset OS_TENANT_NAME")
        print("unset OS_PROJECT_NAME")
        print("unset OS_AUTH_URL")
        print("unset S3_ACCESS_KEY_ID")
        print("unset S3_SECRET_ACCESS_KEY")
        print("unset S3_HOSTNAME")
        print("unset NOVA_ENDPOINT_TYPE")
        print("unset OS_ENDPOINT_TYPE")
        print("unset CINDER_ENDPOINT_TYPE")
        print("unset OS_VOLUME_API_VERSION")
        print("unset OS_IDENTITY_API_VERSION")  #
        print("unset OS_IMAGE_API_VERSION")

    @staticmethod
    def action_read(args):

        if not os.path.isfile(args.read):
            print("{0} file not found.".format(args.read))
            sys.exit(1)

        # check permissions 0600
        st = os.stat(args.read)
        if oct(st.st_mode) > OSEnvController.FILE_PERMISSION:
            print("File {0} has the wrong permissions. \"0600\" are required.".format(args.read))
            sys.exit(1)

        # read from file
        crypto = FileEncryption()
        json_data = crypto.decrypt_configfile(input_file=args.read)

        # save to keyring
        storage = Storage()
        storage.set_data(json_data.decode("utf-8"))

    @staticmethod
    def action_write(args):

        i = 0
        data = {}
        selection_list = ["Add a new OpenStack Environment", "Encode and write file."]

        while True:
            selection = SelectionMenu.get_selection(selection_list)

            if selection == 0:
                osenv = input(
                    "Input environment name for configuration and press [ENTER]: "
                )
                data[i] = json.loads(OSEnvController.add_tenant(name=osenv))
                i += 1

            elif selection == 1:
                print("Encrypt and write file...")
                crypto = FileEncryption()
                crypto.encrypt_configfile(data=json.dumps(data), output_file=args.write)

                if not os.path.isfile(args.write):
                    print("{0} file not found.".format(args.write))
                    break
                    
                try:
                    os.chmod(args.write, 0o600)
                except OSError as e:
                    print("Couldn't change file permissions to 0600. Please change it, otherwise you are not able to read this file. [{0}]".format(e))

                print("File {file} written ...".format(file=args.write))
                print("Finish")
                break
                sys.exit(0)

            elif selection == 2:
                print("Program termination ...")
                # break
                # print(json.dumps(data))
                sys.exit()

    @staticmethod
    def action_edit(args):
        # Check if file exists
        if not os.path.isfile(args.edit):
            print("{0} file not found.".format(args.edit))
            sys.exit(1)
        
        # check permissions 0600
        st = os.stat(args.edit)
        if oct(st.st_mode) > OSEnvController.FILE_PERMISSION:
            print("File {0} has the wrong permissions. \"0600\" are required.".format(args.edit))
            sys.exit(1)

        # read from file
        crypto = FileEncryption()
        json_data = crypto.decrypt_configfile(input_file=args.edit)
        data = json.loads(json_data)

        while True:
            # print("List of available environments:\n")
            if data:
                env_list = []
                for i, osenv in data.items():
                    env = next(iter(osenv)).split("_")[0]
                    env_list.append("Edit {0} environment.".format(env))
            
            # Create menu
            selection_list = ["Add a new OpenStack Environment"]
            selection_list.extend(env_list)
            selection_list.append("Encode and write file {file}.".format(file=args.edit))
            selection = SelectionMenu.get_selection(selection_list)
            
            i = len(env_list)

            if selection == 0:
                osenv = input(
                    "Input environment name for configuration and press [ENTER]: "
                )
                data["{0}".format(i)] = json.loads(OSEnvController.add_tenant(name=osenv))
            elif selection > 0 and selection <= len(env_list):
                print(data["{0}".format(selection - 1)])
                pass
                #OSEnvController.edit_tenant(name=, tenant_data=)

            elif selection == len(env_list) + 1:
                print("Encrypt and write file...")
                print(data)
                crypto.encrypt_configfile(data=json.dumps(data), output_file=args.edit)
                print("Finish")
                break
                sys.exit(0)
            elif selection == len(env_list) + 2:
                print("Program termination ...")
                sys.exit(0)

    
    @staticmethod
    def add_tenant(name):
        otc = Tenant(name)
        otc.set_tenant()
        return otc.export_json(prefix="{0}_".format(otc.environment))

    @staticmethod
    def edit_tenant(name, tenant_data):
        otc = Tenant(name)
        otc.import_data(data=tenant_data, prefix=env)
        return otc.export_json(prefix="{0}_".format(otc.environment))

