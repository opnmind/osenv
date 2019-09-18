#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""Reflects the needed tenant variables for the .ostackrc file."""
import getpass
import json
import re


class Tenant(object):
    """Reflects the needed tenant variables for the .ostackrc file."""

    def __init__(self, environment):
        """Tenant for a given environment.

        Params:
            str: environment Set the nome of the environment for the tenant.

        """
        self.environment = environment
        self.environment_data = ""

        self._OS_USER_DOMAIN_NAME = None
        self._OS_USERNAME = None
        self._OS_PASSWORD = None
        self._OS_TENANT_NAME = None
        self._OS_PROJECT_NAME = None
        self._OS_AUTH_URL = None
        self._S3_ACCESS_KEY_ID = None
        self._S3_SECRET_ACCESS_KEY = None
        self._S3_HOSTNAME = None

        # set defaults
        self._NOVA_ENDPOINT_TYPE = "publicURL"
        self._OS_ENDPOINT_TYPE = "publicURL"
        self._CINDER_ENDPOINT_TYPE = "publicURL"
        self._OS_VOLUME_API_VERSION = 2
        self._OS_IDENTITY_API_VERSION = 3
        self._OS_IMAGE_API_VERSION = 2

    @property
    def OS_USER_DOMAIN_NAME(self):
        """str: OS_USER_DOMAIN_NAME."""
        return self._OS_USER_DOMAIN_NAME

    @OS_USER_DOMAIN_NAME.setter
    def OS_USER_DOMAIN_NAME(self, value):
        # Check for alphanumeric + minus
        if re.match(r"^[\w-]+$", value):
            self._OS_USER_DOMAIN_NAME = value
        else:
            self._OS_USER_DOMAIN_NAME = None

    @property
    def OS_USERNAME(self):
        """str: OS_USERNAME."""
        return self._OS_USERNAME

    @OS_USERNAME.setter
    def OS_USERNAME(self, value):
        self._OS_USERNAME = value

    @property
    def OS_PASSWORD(self):
        """str: OS_PASSWORD."""
        return self._OS_PASSWORD

    @OS_PASSWORD.setter
    def OS_PASSWORD(self, value):
        self._OS_PASSWORD = value

    @property
    def OS_TENANT_NAME(self):
        """str: OS_TENANT_NAME."""
        return self._OS_TENANT_NAME

    @OS_TENANT_NAME.setter
    def OS_TENANT_NAME(self, value):
        self._OS_TENANT_NAME = value

    @property
    def OS_PROJECT_NAME(self):
        """str: OS_PROJECT_NAME."""
        return self._OS_PROJECT_NAME

    @OS_PROJECT_NAME.setter
    def OS_PROJECT_NAME(self, value):
        self._OS_PROJECT_NAME = value

    @property
    def OS_AUTH_URL(self):
        """str: OS_AUTH_URL."""
        return self._OS_AUTH_URL

    @OS_AUTH_URL.setter
    def OS_AUTH_URL(self, value):
        self._OS_AUTH_URL = value

    @property
    def S3_ACCESS_KEY_ID(self):
        """str: S3_ACCESS_KEY_ID."""
        return self._S3_ACCESS_KEY_ID

    @S3_ACCESS_KEY_ID.setter
    def S3_ACCESS_KEY_ID(self, value):
        self._S3_ACCESS_KEY_ID = value

    @property
    def S3_SECRET_ACCESS_KEY(self):
        """str: S3_SECRET_ACCESS_KEY."""
        return self._S3_SECRET_ACCESS_KEY

    @S3_SECRET_ACCESS_KEY.setter
    def S3_SECRET_ACCESS_KEY(self, value):
        self._S3_SECRET_ACCESS_KEY = value

    @property
    def S3_HOSTNAME(self):
        """str: S3_HOSTNAME."""
        return self._S3_HOSTNAME

    @S3_HOSTNAME.setter
    def S3_HOSTNAME(self, value):
        self._S3_HOSTNAME = value

    @property
    def NOVA_ENDPOINT_TYPE(self):
        """str: NOVA_ENDPOINT_TYPE."""
        return self._NOVA_ENDPOINT_TYPE

    @NOVA_ENDPOINT_TYPE.setter
    def NOVA_ENDPOINT_TYPE(self, value):
        self._NOVA_ENDPOINT_TYPE = value

    @property
    def OS_ENDPOINT_TYPE(self):
        """str: OS_ENDPOINT_TYPE."""
        return self._OS_ENDPOINT_TYPE

    @OS_ENDPOINT_TYPE.setter
    def OS_ENDPOINT_TYPE(self, value):
        self._OS_ENDPOINT_TYPE = value

    @property
    def CINDER_ENDPOINT_TYPE(self):
        """str: CINDER_ENDPOINT_TYPE."""
        return self._CINDER_ENDPOINT_TYPE

    @CINDER_ENDPOINT_TYPE.setter
    def CINDER_ENDPOINT_TYPE(self, value):
        self._CINDER_ENDPOINT_TYPE = value

    @property
    def OS_VOLUME_API_VERSION(self):
        """str: OS_VOLUME_API_VERSION."""
        return self._OS_VOLUME_API_VERSION

    @OS_VOLUME_API_VERSION.setter
    def OS_VOLUME_API_VERSION(self, value):
        self._OS_VOLUME_API_VERSION = value

    @property
    def OS_IDENTITY_API_VERSION(self):
        """str: OS_IDENTITY_API_VERSION."""
        return self._OS_IDENTITY_API_VERSION

    @OS_IDENTITY_API_VERSION.setter
    def OS_IDENTITY_API_VERSION(self, value):
        self._OS_IDENTITY_API_VERSION = value

    @property
    def OS_IMAGE_API_VERSION(self):
        """str: OS_IMAGE_API_VERSION."""
        return self._OS_IMAGE_API_VERSION

    @OS_IMAGE_API_VERSION.setter
    def OS_IMAGE_API_VERSION(self, value):
        self._OS_IMAGE_API_VERSION = value

    def export_variable(self, name, prefix=""):
        ret = "export {var_prefix}{var_name}={var_value}\n".format(
            var_prefix=prefix, var_name=name, var_value=eval("self._{0}".format(name))
        )
        return ret

    def import_data(self, data, prefix):
        if isinstance(data, dict):
            self.OS_USER_DOMAIN_NAME = data["{0}_OS_USER_DOMAIN_NAME".format(prefix)]
            self.OS_USERNAME = data["{0}_OS_USERNAME".format(prefix)]
            self.OS_PASSWORD = data["{0}_OS_PASSWORD".format(prefix)]
            self.OS_TENANT_NAME = data["{0}_OS_TENANT_NAME".format(prefix)]
            self.OS_PROJECT_NAME = data["{0}_OS_PROJECT_NAME".format(prefix)]
            self.OS_AUTH_URL = data["{0}_OS_AUTH_URL".format(prefix)]
            self.S3_ACCESS_KEY_ID = data["{0}_S3_ACCESS_KEY_ID".format(prefix)]
            self.S3_SECRET_ACCESS_KEY = data["{0}_S3_SECRET_ACCESS_KEY".format(prefix)]
            self.S3_HOSTNAME = data["{0}_S3_HOSTNAME".format(prefix)]
            self.NOVA_ENDPOINT_TYPE = data["{0}_NOVA_ENDPOINT_TYPE".format(prefix)]
            self.OS_ENDPOINT_TYPE = data["{0}_OS_ENDPOINT_TYPE".format(prefix)]
            self.CINDER_ENDPOINT_TYPE = data["{0}_CINDER_ENDPOINT_TYPE".format(prefix)]
            self.OS_VOLUME_API_VERSION = data[
                "{0}_OS_VOLUME_API_VERSION".format(prefix)
            ]
            self.OS_IDENTITY_API_VERSION = data[
                "{0}_OS_IDENTITY_API_VERSION".format(prefix)
            ]
            self.OS_IMAGE_API_VERSION = data["{0}_OS_IMAGE_API_VERSION".format(prefix)]
        else:
            print("IMPORT: Wrong data.")

    def export_ostackrc(self, prefix=""):
        ostackrc = ""
        ostackrc += self.export_variable(name="OS_USER_DOMAIN_NAME", prefix=prefix)
        ostackrc += self.export_variable(name="OS_USERNAME", prefix=prefix)
        ostackrc += self.export_variable(name="OS_PASSWORD", prefix=prefix)
        ostackrc += self.export_variable(name="OS_TENANT_NAME", prefix=prefix)
        ostackrc += self.export_variable(name="OS_PROJECT_NAME", prefix=prefix)
        ostackrc += self.export_variable(name="OS_AUTH_URL", prefix=prefix)
        ostackrc += self.export_variable(name="NOVA_ENDPOINT_TYPE", prefix=prefix)
        ostackrc += self.export_variable(name="OS_ENDPOINT_TYPE", prefix=prefix)
        ostackrc += self.export_variable(name="CINDER_ENDPOINT_TYPE", prefix=prefix)
        ostackrc += self.export_variable(name="OS_VOLUME_API_VERSION", prefix=prefix)
        ostackrc += self.export_variable(name="OS_IDENTITY_API_VERSION", prefix=prefix)
        ostackrc += self.export_variable(name="OS_IMAGE_API_VERSION", prefix=prefix)
        ostackrc += self.export_variable(name="S3_ACCESS_KEY_ID", prefix=prefix)
        ostackrc += self.export_variable(name="S3_SECRET_ACCESS_KEY", prefix=prefix)
        ostackrc += self.export_variable(name="S3_HOSTNAME", prefix=prefix)

        return ostackrc

    def export_json(self, prefix=""):
        json_data = {
            "{str_prefix}OS_USER_DOMAIN_NAME".format(str_prefix=prefix): "{0}".format(
                self.OS_USER_DOMAIN_NAME
            ),
            "{str_prefix}OS_USERNAME".format(str_prefix=prefix): "{0}".format(
                self.OS_USERNAME
            ),
            "{str_prefix}OS_PASSWORD".format(str_prefix=prefix): "{0}".format(
                self.OS_PASSWORD
            ),
            "{str_prefix}OS_TENANT_NAME".format(str_prefix=prefix): "{0}".format(
                self.OS_TENANT_NAME
            ),
            "{str_prefix}OS_PROJECT_NAME".format(str_prefix=prefix): "{0}".format(
                self.OS_PROJECT_NAME
            ),
            "{str_prefix}OS_AUTH_URL".format(str_prefix=prefix): "{0}".format(
                self.OS_AUTH_URL
            ),
            "{str_prefix}NOVA_ENDPOINT_TYPE".format(str_prefix=prefix): "{0}".format(
                self.NOVA_ENDPOINT_TYPE
            ),
            "{str_prefix}OS_ENDPOINT_TYPE".format(str_prefix=prefix): "{0}".format(
                self.OS_ENDPOINT_TYPE
            ),
            "{str_prefix}CINDER_ENDPOINT_TYPE".format(str_prefix=prefix): "{0}".format(
                self.CINDER_ENDPOINT_TYPE
            ),
            "{str_prefix}OS_VOLUME_API_VERSION".format(str_prefix=prefix): "{0}".format(
                self.OS_VOLUME_API_VERSION
            ),
            "{str_prefix}OS_IDENTITY_API_VERSION".format(
                str_prefix=prefix
            ): "{0}".format(self.OS_IDENTITY_API_VERSION),
            "{str_prefix}OS_IMAGE_API_VERSION".format(str_prefix=prefix): "{0}".format(
                self.OS_IMAGE_API_VERSION
            ),
            "{str_prefix}S3_ACCESS_KEY_ID".format(str_prefix=prefix): "{0}".format(
                self.S3_ACCESS_KEY_ID
            ),
            "{str_prefix}S3_SECRET_ACCESS_KEY".format(str_prefix=prefix): "{0}".format(
                self.S3_SECRET_ACCESS_KEY
            ),
            "{str_prefix}S3_HOSTNAME".format(str_prefix=prefix): "{0}".format(
                self.S3_HOSTNAME
            ),
        }
        return json.dumps(json_data)

    def set_tenant(self):
        print("---# Set up ostackrc for ENV: {0} #---".format(self.environment))
        self.OS_USER_DOMAIN_NAME = input(
            "Input your OS_USER_DOMAIN_NAME and press [ENTER]: "
        )
        self.OS_USERNAME = input("Input your OS_USERNAME and press [ENTER]: ")

        try:
            self.OS_PASSWORD = getpass.getpass(
                prompt="Input your OS_PASSWORD and press [ENTER]: "
            )
        except Exception as error:
            print("ERROR OS_PASSWORD", error)

        self.OS_TENANT_NAME = input("Input your OS_TENANT_NAME and press [ENTER]: ")
        self.OS_PROJECT_NAME = input("Input your OS_PROJECT_NAME and press [ENTER]: ")
        self.OS_AUTH_URL = input("Input your OS_AUTH_URL and press [ENTER]: ")
        self.S3_ACCESS_KEY_ID = input("Input your S3_ACCESS_KEY_ID and press [ENTER]: ")

        try:
            self.S3_SECRET_ACCESS_KEY = getpass.getpass(
                prompt="Input your S3_SECRET_ACCESS_KEY and press [ENTER]: "
            )
        except Exception as error:
            print("ERROR S3_SECRET_ACCESS_KEY", error)

        self.S3_HOSTNAME = input("Input your S3_HOSTNAME and press [ENTER]: ")

        print("---# EOF ENV: {0} #---".format(self.environment))


if __name__ == "__main__":
    pass
    """
    otc.OS_USER_DOMAIN_NAME = "OTC-EU-DE-00000000001000035466"
    otc.OS_USERNAME = "roschil_api"
    otc.OS_PASSWORD = "xyz"
    otc.OS_TENANT_NAME = "eu-de"
    otc.OS_PROJECT_NAME = "eu-de"
    otc.OS_AUTH_URL = "https://iam.eu-de.otc.t-systems.com:443/v3"
    otc.S3_ACCESS_KEY_ID = "xyz"
    otc.S3_SECRET_ACCESS_KEY = "xyz"
    otc.S3_HOSTNAME = "obs.eu-de.otc.t-systems.com"
    """
    """
    otc = Tenant('PROD')
    otc.set_tenant()

    preprod = Tenant('PREPROD')
    preprod.set_tenant()

    env_prod = otc.export_ostackrc(prefix="{}_".format(otc.environment))
    env_preprod = preprod.export_ostackrc(prefix="{}_".format(preprod.environment))

    env = "{0}{1}".format(env_preprod, env_prod)
    #print(env)
    """
