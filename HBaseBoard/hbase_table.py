# -*- coding: utf-8 -*-

class _TableScanner(object):
    def __init__(self, table):
        self.table_scan = table.scan()

    def __iter__(self):
        return self

    def next(self):
        val = self.table_scan.next()
        return val


class HBaseTable(object):
    def __init__(self, table_name, hbase_wrapper):
        self.table_name = table_name
        self.table = hbase_wrapper.get_table(self.table_name)

    def put(self, insert_list):
        for key, values in insert_list:
            self.table.put(key, values)

    def scan(self):
        return _TableScanner(self.table)
