#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `hbase_wraqpper` module.
"""
import pytest

from HBaseBoard.hbase_wrapper import HBaseWrapper
import happybase as hb


class TestHBaseWrapper(object):
    def setup(self):
        self.hb_wrapper = HBaseWrapper()
        self.hb_wrapper.delete_all_tables()
        self.hbase_con = hb.Connection()

    def teardown(self):
        self.hb_wrapper.delete_all_tables()
        self.hb_wrapper.close_connection()
        self.hbase_con.close()

    def test_get_table_returns_table(self):
        self.hb_wrapper.create_default_table(
            "test_table",
            dict(cf1=dict(), cf2=dict())
        )

        returned_table = self.hb_wrapper.get_table("test_table")
        families = returned_table.families().keys()
        assert 2 == len(families)
        assert "cf1" in families
        assert "cf1" in families

    def test_get_table_raises_error_if_table_doesnt_exist(self):
        self.hb_wrapper.create_default_table(
            "test_table",
            dict(cf1=dict(), cf2=dict())
        )

        with pytest.raises(ValueError):
            self.hb_wrapper.get_table("new_table")

    def test_get_empty_table_list(self):
        assert [] == HBaseWrapper().get_tables_list()

    def test_get_single_list(self):
        table_name_list = ["test_table1", "test_table2"]
        self.hbase_con.create_table(table_name_list[0], dict(cf=dict()))
        self.hbase_con.create_table(table_name_list[1], dict(cf=dict()))
        assert table_name_list == self.hb_wrapper.get_tables_list()

    def test_clear_all_tables(self):
        self.hbase_con.create_table("test_table1", dict(cf=dict()))
        self.hbase_con.create_table("test_table2", dict(cf=dict()))
        self.hb_wrapper.delete_all_tables()
        assert 0 == len(self.hb_wrapper.get_tables_list())

    def test_create_simple_table(self):
        self.hb_wrapper.create_default_table("test_table")
        assert ["test_table"] == self.hb_wrapper.get_tables_list()
        assert ["cf"] == self.hbase_con.table("test_table").families().keys()

    def test_create_table_with_schema(self):
        self.hb_wrapper.create_default_table(
            "test_table",
            dict(cf1=dict(), cf2=dict())
        )
        assert ["test_table"] == self.hb_wrapper.get_tables_list()
        families = self.hbase_con.table("test_table").families().keys()
        assert 2 == len(families)
        assert "cf1" in families
        assert "cf1" in families
