#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Tests for `hbase_wraqpper` module.
"""
from mock import Mock
import pytest

from HBaseBoard.hbase_wrapper import HBaseWrapper


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.setattr("happybase.Connection", Mock())


@pytest.mark.unittest
class TestHBaseWrapper(object):
    def setup(self):
        self.hb_wrapper = HBaseWrapper()
        self.hb_wrapper.hbase_con = Mock()

    def test_default_table_creation(self):
        self.hb_wrapper.create_default_table("test_table")
        self.hb_wrapper.hbase_con.create_table.assert_called_with(
            "test_table", dict(cf=dict()))

    def test_create_table_with_schema(self):
        cf_dict = dict(cf1=dict(), cf2=dict())
        self.hb_wrapper.create_default_table("test_table", cf_dict)
        self.hb_wrapper.hbase_con.create_table.assert_called_with(
            "test_table", cf_dict)

    def test_get_table_returns_table(self):
        table_name = "test_table"
        self.hb_wrapper.hbase_con.tables.return_value = [table_name]
        self.hb_wrapper.get_table(table_name)

        self.hb_wrapper.hbase_con.table.assert_called_with(table_name)

    def test_get_table_raises_error_if_table_doesnt_exist(self):
        self.hb_wrapper.hbase_con.tables.return_value = ["some_table"]
        with pytest.raises(ValueError):
            self.hb_wrapper.get_table("new_table")

    def test_get_table_list(self):
        self.hb_wrapper.hbase_con.tables.return_value = ["table_name"]
        assert ["table_name"] == self.hb_wrapper.get_tables_list()

    def test_clear_all_tables(self):
        self.hb_wrapper.hbase_con.tables.return_value = [
            "test_table1", "test_table2"
        ]
        self.hb_wrapper.delete_all_tables()

        assert 2 == self.hb_wrapper.hbase_con.delete_table.call_count
        self.hb_wrapper.hbase_con.delete_table.assert_any_call(
            "test_table1", disable=True)
        self.hb_wrapper.hbase_con.delete_table.assert_any_call(
            "test_table2", disable=True)
