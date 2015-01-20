#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `hbase_table` module.
"""
import pytest

from HBaseBoard.hbase_table import HBaseTable
from HBaseBoard.hbase_wrapper import HBaseWrapper


class TestHBaseTableClass(object):
    def setup(self):
        self.hb_wrapper = HBaseWrapper()
        self.hb_wrapper.delete_all_tables()
        self.hb_wrapper.create_default_table("test_table")

    def teardown(self):
        self.hb_wrapper.delete_all_tables()
        self.hb_wrapper.close_connection()

    def test_raises_error_if_no_table_exists(self):
        with pytest.raises(ValueError):
            HBaseTable("ghost", self.hb_wrapper)

    def test_scan_returns_iterable_that_scans_a_table(self):
        my_table = HBaseTable("test_table", self.hb_wrapper)
        test_val1 = ("key1", {"cf:first_name": "bugs", "cf:last_name": "bunny"})
        test_val2 = ("key2", {"cf:first_name": "daffy", "cf:last_name": "duck"})
        my_table.put([test_val1, test_val2])

        table_vals = []
        for value in my_table.scan():
            table_vals.append(value)

        assert 2 == len(table_vals)
        assert test_val1 in table_vals
        assert test_val2 in table_vals

    def test_scan_accepts_filter_on_keys(self):
        my_table = HBaseTable("test_table", self.hb_wrapper)
        test_val1 = ("key1_matches",
                     {"cf:first_name": "bugs", "cf:last_name": "bunny"})
        test_val2 = ("key2_does_not_match",
                     {"cf:first_name": "daffy", "cf:last_name": "duck"})
        test_val3 = ("key3_matches",
                     {"cf:first_name": "porky", "cf:last_name": "pig"})
        test_val4 = ("key4_matches_not_expected",
                     {"cf:first_name": "goofy", "cf:last_name": "dog"})
        my_table.put([test_val1, test_val2, test_val3, test_val4])

        table_vals = []
        for value in my_table.scan(key="matches$"):
            table_vals.append(value)

        assert 2 == len(table_vals)
        assert test_val1 in table_vals
        assert test_val3 in table_vals

    def test_scan_accepts_custom_max_count(self):
        my_table = HBaseTable("test_table", self.hb_wrapper)
        test_val1 = ("key1", {"cf:first_name": "bugs", "cf:last_name": "bunny"})
        test_val2 = ("key2", {"cf:first_name": "daffy", "cf:last_name": "duck"})
        test_val3 = ("key3", {"cf:first_name": "porky", "cf:last_name": "pig"})
        test_val4 = ("key4", {"cf:first_name": "goofy", "cf:last_name": "dog"})
        my_table.put([test_val1, test_val2, test_val3, test_val4])

        table_vals = []
        for value in my_table.scan(max_count=3):
            table_vals.append(value)

        assert 3 == len(table_vals)

    def test_scan_counts_only_the_fields_that_match(self):
        my_table = HBaseTable("test_table", self.hb_wrapper)
        test_val1 = ("key1_matches",
                     {"cf:first_name": "bugs", "cf:last_name": "bunny"})
        test_val2 = ("key2_does_not_match",
                     {"cf:first_name": "daffy", "cf:last_name": "duck"})
        test_val3 = ("key3_matches",
                     {"cf:first_name": "porky", "cf:last_name": "pig"})
        test_val4 = ("key4_another_one_matches",
                     {"cf:first_name": "goofy", "cf:last_name": "dog"})
        my_table.put([test_val1, test_val2, test_val3, test_val4])

        table_vals = []
        for value in my_table.scan(key="matches$", max_count=2):
            table_vals.append(value)

        assert 2 == len(table_vals)
        assert test_val1 in table_vals
        assert test_val3 in table_vals
