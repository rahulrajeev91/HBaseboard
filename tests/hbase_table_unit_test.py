#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for `hbase_table` module.
"""
import pytest
from mock import Mock

from HBaseBoard.hbase_table import HBaseTable

@pytest.mark.unittest
class TestHBaseTableClass(object):
    def setup(self):
        self.table_mock = Mock()
        self.hb_wrapper = Mock()
        self.hb_wrapper.get_tables_list.return_value = ["test_table"]
        self.hb_wrapper.get_table.return_value = self.table_mock
        self.table_mock.scan.return_value = iter([])

    def test_scan_returns_iterable_that_scans_a_table(self):
        my_table = HBaseTable("test_table", self.hb_wrapper)
        test_val1 = ("key1", {"cf:first_name": "bugs", "cf:last_name": "bunny"})
        test_val2 = ("key2", {"cf:first_name": "daffy", "cf:last_name": "duck"})
        self.table_mock.scan.return_value = iter([test_val1, test_val2])

        table_vals = []
        for value in my_table.scan():
            table_vals.append(value)

        self.table_mock.scan.assert_called_with()
        assert 2 == len(table_vals)
        assert test_val1 in table_vals
        assert test_val2 in table_vals

    def test_scan_accepts_filter_on_keys(self):
        pass
        #my_table = HBaseTable("test_table", self.hb_wrapper)

        #my_table.scan(filter=[("key_regex", "matches$")]).next()

        #self.table_mock.scan.assert_called_with(filter="RowFilter(=, 'regexstring:matches$')")

    def test_scan_accepts_custom_max_count(self):
        my_table = HBaseTable("test_table", self.hb_wrapper)
        test_val1 = ("key1", {"cf:first_name": "bugs", "cf:last_name": "bunny"})
        test_val2 = ("key2", {"cf:first_name": "daffy", "cf:last_name": "duck"})
        test_val3 = ("key3", {"cf:first_name": "porky", "cf:last_name": "pig"})
        test_val4 = ("key4", {"cf:first_name": "goofy", "cf:last_name": "dog"})
        self.table_mock.scan.return_value = iter([test_val1, test_val2, test_val3, test_val4])

        table_vals = []
        for value in my_table.scan(max_count=3):
            table_vals.append(value)

        assert 3 == len(table_vals)
