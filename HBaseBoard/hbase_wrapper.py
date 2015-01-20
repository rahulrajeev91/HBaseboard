# -*- coding: utf-8 -*-
import happybase as hb
import config


class HBaseWrapper(object):
    def __init__(self, host="localhost", port=9090):
        self.hbase_con = hb.Connection(
            host=host,
            port=port,
            timeout=config.CONNECTION_TIMEOUT
        )

    def close_connection(self):
        return self.hbase_con.close()

    def get_tables_list(self):
        return self.hbase_con.tables()

    def delete_all_tables(self):
        for table_name in self.get_tables_list():
            self.hbase_con.delete_table(table_name, disable=True)

    def create_default_table(self, table_name, families=dict(cf=dict())):
        self.hbase_con.create_table(table_name, families)

    def get_table(self, table_name):
        if table_name not in self.get_tables_list():
            raise ValueError("Table \"{}\" does not exist". format(table_name))
        return self.hbase_con.table(table_name)
