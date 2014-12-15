# -*- coding: utf-8 -*-

class HBaseTable(object):
    def __init__(self, table_name, hbase_wrapper):
        self.table_name = table_name
        self.table = hbase_wrapper.get_table(self.table_name)

    def _put(self, *args, **kwargs):
        self.table.put(args, kwargs)
