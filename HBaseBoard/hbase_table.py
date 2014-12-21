# -*- coding: utf-8 -*-
import re


class _TableScanner(object):
    def __init__(self, table):
        self.key_regex = re.compile(".*")
        self.table_scan = table.scan()

    def __iter__(self):
        return self

    def next(self):
        key, val = self.table_scan.next()
        if self.key_regex.search(key):
            return (key, val)
        return self.next()

    def add_key_regex(self, regex):
        self.key_regex = re.compile(regex)


class HBaseTable(object):
    def __init__(self, table_name, hbase_wrapper):
        self.table_name = table_name
        self.table = hbase_wrapper.get_table(self.table_name)

    def put(self, insert_list):
        for key, values in insert_list:
            self.table.put(key, values)

    def scan(self, key=None):
        table_scanner = _TableScanner(self.table)
        if key:
            table_scanner.add_key_regex(key)
        return table_scanner
