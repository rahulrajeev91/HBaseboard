#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `hbase_wraqpper` module.
"""
import pytest

from HBaseBoard.hbase_table import HBaseTable
from HBaseBoard.hbase_wrapper import HBaseWrapper
import happybase as hb


class TestHBaseTableClass(object):
    def setup(self):
        self.hbase_con = hb.Connection()
        self.hb_wrapper = HBaseWrapper()
        self.hb_wrapper.delete_all_tables()
        self.hb_wrapper.create_default_table("test_table")

    def test_raises_error_if_no_table_exists(self):
        with pytest.raises(ValueError):
            HBaseTable("ghost", self.hb_wrapper)

    def test_scan_returns_iterable_that_scans_a_table(self):
        my_table = HBaseTable("test_table", self.hb_wrapper)
        value_dict1 = {"cf:first_name": "bugs", "cf:last_name": "bunny"}
        value_dict2 = {"cf:first_name": "daffy", "cf:last_name": "duck"}
        my_table._put("key1", value_dict1)
        my_table._put("key2", value_dict2)
