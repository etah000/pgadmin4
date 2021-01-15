##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""Database helper utilities"""

from flask import render_template


def parse_sec_labels_from_db(db_sec_labels):
    """
    Function to format the output for security label.

    Args:
        db_sec_labels : Security Label Array in (provider=label) format

    Returns:
        Security Label Object in below format:
            {'seclabels': [{'provider': 'provider_name', 'label':
            'label'},...]}
    """
    sec_lbls = []

    if db_sec_labels is not None:
        for sec in db_sec_labels:
            import re
            sec = re.search(r'([^=]+)=(.*$)', sec)
            sec_lbls.append({
                'provider': sec.group(1),
                'label': sec.group(2)
            })

    return {"seclabels": sec_lbls}


def parse_variables_from_db(db_variables):
    """
    Function to format the output for variables.

    Args:
        db_variables: Variable object

            Expected Object Format:
                [
                    {
                    'setconfig': Variable Config Parameters,
                    'user_name': User Name,
                    'db_name': Database Name
                    },...
                ]
            where:
                user_name and database are optional
    Returns:
        Variable Object in below format:
            {
            'variables': [
                {'name': 'var_name', 'value': 'var_value',
                'user_name': 'user_name', 'database': 'database_name'},
                ...]
            }
            where:
                user_name and database are optional
    """
    variables_lst = []

    if db_variables is not None:
        for row in db_variables:
            if 'setconfig' in row and row['setconfig'] is not None:
                for d in row['setconfig']:
                    var_name, var_value = d.split("=")
                    # Because we save as boolean string in db so it needs
                    # conversion
                    if var_value == 'false' or var_value == 'off':
                        var_value = False

                    var_dict = {
                        'name': var_name,
                        'value': var_value
                    }
                    if 'user_name' in row:
                        var_dict['role'] = row['user_name']
                    if 'db_name' in row:
                        var_dict['database'] = row['db_name']

                    variables_lst.append(var_dict)

    return {"variables": variables_lst}


class ClusterReader:
    """
    ClusterReader Class.

    This class includes common utilities for system.clusters.

    Methods:
    -------
    * get_clusters(conn, ):
      - Returns clusters.
    """

    def get_clusters(self, conn, ):
        """

        Args:
            conn: Connection Object
        """
        # Check if template path is already set or not
        # if not then we will set the template path here
        if not hasattr(self, 'cluster_template_path'):
            self.data_type_template_path = 'cluster/sql/' + (
                '#{0}#'.format(self.manager.version)
            )
        SQL = render_template(
            "/".join([self.data_type_template_path, 'get_clusters.sql']),
        )
        status, res = conn.execute_2darray(SQL)

        if not status:
            return status, res

        return True, res['rows']



class EngineReader:
    """
    EngineReader Class.

    This class includes common utilities for system.table_engines.

    Methods:
    -------
    * get_engines(conn, ):
      - Returns engines.
    """

    def get_engines(self, conn, ):
        """
        Returns data-types including calculation for Length and Precision.

        Args:
            conn: Connection Object
            condition: condition to restrict SQL statement
            add_serials: If you want to serials type
            schema_oid: If needed pass the schema OID to restrict the search
        """

        # Check if template path is already set or not
        # if not then we will set the template path here
        if not hasattr(self, 'engine_template_path'):
            self.data_type_template_path = 'engine/sql/' + (
                '#{0}#'.format(self.manager.version)
            )
        SQL = render_template(
            "/".join([self.data_type_template_path, 'get_engines.sql']),
        )
        status, res = conn.execute_2darray(SQL)

        if not status:
            return status, res

        return True, res['rows']