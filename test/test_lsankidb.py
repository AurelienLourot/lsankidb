# -*- coding: utf-8 -*-
# pylint: disable=no-self-use,invalid-name

import sqlite3

from unittest import mock, TestCase

from src import lsankidb

class LsankidbTests(TestCase):
    @mock.patch('src.lsankidb.print')
    @mock.patch('src.lsankidb.Db')
    @mock.patch('src.lsankidb._find_db_path')
    @mock.patch('src.lsankidb._parse_args')
    def test_main_finds_db_and_prints_it(self, mock_parse_args, mock_find_db_path, mock_db,
                                         mock_print):
        mock_parse_args.return_value.PATH = None
        mock_find_db_path.return_value = '/path/to/db.anki2'
        mock_db.side_effect = ['hello']

        lsankidb.main()

        mock_db.assert_called_once_with(mock_find_db_path.return_value)
        mock_print.assert_has_calls([mock.call('hello')])

    @mock.patch('src.lsankidb.print')
    @mock.patch('src.lsankidb.Db')
    @mock.patch('src.lsankidb._parse_args')
    def test_main_prints_passed_db(self, mock_parse_args, mock_db, mock_print):
        mock_parse_args.return_value.PATH = '/path/to/db.anki2'
        mock_db.side_effect = ['hello']

        lsankidb.main()

        mock_db.assert_called_once_with(mock_parse_args.return_value.PATH)
        mock_print.assert_has_calls([mock.call('hello')])

    @mock.patch('src.lsankidb._find_db_path')
    @mock.patch('src.lsankidb._parse_args')
    def test_main_fails_if_no_db_found(self, mock_parse_args, mock_find_db_path):
        mock_parse_args.return_value.PATH = None
        mock_find_db_path.return_value = None

        with self.assertRaises(SystemExit):
            lsankidb.main()

    @mock.patch('src.lsankidb.Db')
    @mock.patch('src.lsankidb._parse_args')
    def test_main_fails_with_corrupted_db(self, mock_parse_args, mock_db):
        mock_parse_args.return_value.PATH = '/path/to/db.anki2'
        mock_db.side_effect = sqlite3.OperationalError('error')

        with self.assertRaises(sqlite3.OperationalError):
            lsankidb.main()
