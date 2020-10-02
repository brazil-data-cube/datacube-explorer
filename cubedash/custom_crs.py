"""
File with features to handle arbitrary definitions that may be needed depending on the
context in which the datacube-explorer is being applied
"""

import json
from typing import Optional
from pyproj import CRS as PJCRS


class CustomCRSConfigHandlerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CustomCRSConfigHandlerSingleton(metaclass=CustomCRSConfigHandlerMeta):
    """Class to handle a custom crs in JSON format. This class is a singleton implementation. With this, the context
    can be maintained by the class, allowing its use in different places of the code

    See:
        https://refactoring.guru/design-patterns/singleton
    """

    _configfile = None
    _configfile_obj = None

    def __init__(self, configfile=None):
        if configfile:
            self._configfile = configfile

    def configure_database_with_custom_crs(self, index) -> None:
        """Function to configure database using custom EPSG
        :return:
        """
        custom_crs = self._load_configfile()

        for custom_crs_code_and_entity in custom_crs:
            custom_crs_entity, custom_crs_code = custom_crs_code_and_entity.split(":")
            resproxy = index._db._engine.execute(
                f"SELECT * FROM spatial_ref_sys WHERE srid = {custom_crs_code}"
            )

            resset = resproxy.first()
            if not resset:
                custom_crs_string = PJCRS(custom_crs[custom_crs_code_and_entity])

                index._db._engine.execute(
                    "INSERT INTO spatial_ref_sys VALUES ({}, '{}', '{}', '{}', '{}');".format(
                        custom_crs_code,
                        custom_crs_entity.upper(),
                        custom_crs_code,
                        custom_crs_string.to_wkt(),
                        custom_crs_string.to_proj4(),
                    )
                )

    def _load_configfile(self):
        """Load configfile with custom CRS definitions
        """

        if not self._configfile_obj:
            try:
                with open(self._configfile, 'r') as configfilestream:
                    self._configfile_obj = json.load(configfilestream)
            except Exception:
                raise RuntimeError('''
                Based on the definitions of your projections it was identified the need to use custom CRS. 
                To do so, define the file with the customized CRS in the CLI of cubedash
                ''')
        return self._configfile_obj

    def get_custom_epsg(self, crs_str: str) -> Optional[str]:
        """This function defines the EPSG based on the custom CRS String defined by users in crs's config file

        Args:
            crs_str (str): crs in projstring or wkt format
        Returns:
            Optional[str]: If crs_str is defined by user, a custom EPSG code is returned. This EPSG custom code must
            have registered in PostgreSQL database
        """
        custom_crs_code = self._load_configfile()

        pyprojobj = PJCRS(crs_str)
        for custom_epsg in custom_crs_code:
            if pyprojobj == PJCRS(custom_crs_code[custom_epsg]):
                return custom_epsg
        raise RuntimeError('Custom EPSG is not defined for {}'.format(crs_str))

    def get_crs_definition_from_custom_epsg(self, custom_epsg: str) -> Optional[str]:
        """Based on user definitions, this function retrieves the string definition from a CRS using the
        custom EPSG code
        Args:
            custom_epsg (str): A custom EPSG string
        Returns:
            Optional[str]: A custom CRS definition string
        """

        custom_crs_code = self._load_configfile()

        if not custom_crs_code.get(custom_epsg):
            raise RuntimeError('A custom CRS definition to {} is not defined!'.format(custom_epsg))
        return custom_crs_code.get(custom_epsg)
