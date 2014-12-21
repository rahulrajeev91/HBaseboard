# -*- coding: utf-8 -*-
import re
import config


class _TableScanner(object):
    def __init__(self, table, max_count):
        self.key_regex = re.compile(".*")
        self.table_scan = table.scan()
        self.max_count = max_count
        self.count = 0

    def __iter__(self):
        return self

    def next(self):
        key, val = self.table_scan.next()
        if not self.key_regex.search(key):
            return self.next()

        self.count += 1
        if self.count > self.max_count:
            raise StopIteration

        return (key, val)

    def add_key_regex(self, regex):
        self.key_regex = re.compile(regex)


class HBaseTable(object):
    def __init__(self, table_name, hbase_wrapper):
        self.table_name = table_name
        self.table = hbase_wrapper.get_table(self.table_name)

    def put(self, insert_list):
        for key, values in insert_list:
            self.table.put(key, values)

    def scan(self, key=None, max_count=config.MAX_SCAN_COUNT):
        table_scanner = _TableScanner(self.table, max_count)
        if key:
            table_scanner.add_key_regex(key)
        return table_scanner
