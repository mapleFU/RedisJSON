# -*- coding: utf-8 -*-
import sys
import os
import redis
import json
from RLTest import Env

from common import *
from includes import *

from RLTest import Defaults

from functools import reduce

Defaults.decode_responses = True


class testResp3():
    def __init__(self):
        self.env = Env(protocol=3)

    def test_resp3_set_get_json_format(self):
        r = self.env
        r.skipOnVersionSmaller('7.0')

        r.assertTrue(r.execute_command('SET', 'test_not_JSON', 'test_not_JSON'))

        # Test JSON.SET RESP3
        r.assertOk(r.execute_command('JSON.SET', 'test_resp3', '$', '{"a1":{"b":{"c":true,"d":null}},"a2":{"b":{"c":2}}}'))

        # Test JSON.GET RESP3
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'JSON', '$'), [['{"a1":{"b":{"c":true,"d":null}},"a2":{"b":{"c":2}}}']])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'JSON', '$..b'), [['{"c":true,"d":null}', '{"c":2}']])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'JSON', '$.a1', '$.a2'),  [['{"b":{"c":true,"d":null}}'], ['{"b":{"c":2}}']])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'JSON', '$.a1', '$.a3', '$.a2'),  [['{"b":{"c":true,"d":null}}'], [], ['{"b":{"c":2}}']])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'JSON', '$.a3'), [[]])

        # TEST JSON.GET with none existent key
        r.assertEqual(r.execute_command('JSON.GET', 'test_no_such_key', '$.a3'), None)

        # TEST JSON.GET with not a JSON key
        r.expect('JSON.GET', 'test_not_JSON', '$.a3').raiseError()

    def test_resp3_set_get_expand_format(self):
        r = self.env
        r.skipOnVersionSmaller('7.0')

        r.assertTrue(r.execute_command('SET', 'test_not_JSON', 'test_not_JSON'))

        # Test JSON.SET RESP3
        r.assertOk(r.execute_command('JSON.SET', 'test_resp3', '$', '{"a1":{"b":{"c":true,"d":null}},"a2":{"b":{"c":2, "e":[1,true, {"f":null}]}}}'))

        # Test JSON.GET RESP3
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'EXPAND', '$'), [[{'a1': {'b': {'c': True, 'd': None}}, 'a2': {'b': {'e': [1, True, {'f': None}], 'c': 2}}}]])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'EXPAND','$..b'), [[{'d': None, 'c': True}, {'c': 2, 'e': [1, True, {'f': None}]}]])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'EXPAND','$.a1', '$.a2'),  [[{'b': {'d': None, 'c': True}}], [{'b': {'e': [1, True, {'f': None}], 'c': 2}}]])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'EXPAND','$.a1', '$.a3', '$.a2'),  [[{'b': {'c': True, 'd': None}}], [], [{'b': {'c': 2, 'e': [1, True, {'f': None}]}}]])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'EXPAND','$.a3'), [[]])

        # Test JSON.GET RESP3 with default format (EXPAND)
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', '$'), [[{'a1': {'b': {'c': True, 'd': None}}, 'a2': {'b': {'e': [1, True, {'f': None}], 'c': 2}}}]])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3','$..b'), [[{'d': None, 'c': True}, {'c': 2, 'e': [1, True, {'f': None}]}]])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3','$.a1', '$.a2'),  [[{'b': {'d': None, 'c': True}}], [{'b': {'e': [1, True, {'f': None}], 'c': 2}}]])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3','$.a1', '$.a3', '$.a2'),  [[{'b': {'c': True, 'd': None}}], [], [{'b': {'c': 2, 'e': [1, True, {'f': None}]}}]])
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3','$.a3'), [[]])

        # TEST JSON.GET with none existent key
        r.assertEqual(r.execute_command('JSON.GET', 'test_no_such_key', 'FORMAT', 'EXPAND','$.a3'), None)

        # TEST JSON.GET with not a JSON key
        r.expect('JSON.GET', 'test_not_JSON', 'FORMAT', 'EXPAND','$.a3').raiseError()


    def test_resp3_set_get_string_format(self):
        r = self.env
        r.skipOnVersionSmaller('7.0')

        r.assertTrue(r.execute_command('SET', 'test_not_JSON', 'test_not_JSON'))

        # Test JSON.SET RESP3
        r.assertOk(r.execute_command('JSON.SET', 'test_resp3', '$', '{"a1":{"b":{"c":true,"d":null}},"a2":{"b":{"c":2}}}'))

        # Test JSON.GET RESP3
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'STRING', '$'), '[{"a1":{"b":{"c":true,"d":null}},"a2":{"b":{"c":2}}}]')
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'STRING', '$..b'), '[{"c":true,"d":null},{"c":2}]')
        r.assertEqual(json.loads(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'STRING', '$.a1', '$.a2')), {"$.a2":[{"b":{"c":2}}],"$.a1":[{"b":{"c":True,"d":None}}]})
        r.assertEqual(json.loads(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'STRING', '.a1', '$.a2')), {"$.a2":[{"b":{"c":2}}],".a1":[{"b":{"c":True,"d":None}}]})
        r.assertEqual(json.loads(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'STRING', '$.a1', '$.a3', '$.a2')),  {"$.a3":[],"$.a2":[{"b":{"c":2}}],"$.a1":[{"b":{"c":True,"d":None}}]})
        r.assertEqual(r.execute_command('JSON.GET', 'test_resp3', 'FORMAT', 'STRING', '$.a3'), '[]')

        # TEST JSON.GET with none existent key
        r.assertEqual(r.execute_command('JSON.GET', 'test_no_such_key', '$.a3'), None)

        # TEST JSON.GET with not a JSON key
        r.expect('JSON.GET', 'test_not_JSON', '$.a3').raiseError()


    # Test JSON.DEL RESP3
    def test_resp_json_del(self):
        r = self.env
        r.skipOnVersionSmaller('7.0')

        r.assertTrue(r.execute_command('SET', 'test_not_JSON', 'test_not_JSON'))

        r.assertOk(r.execute_command('JSON.SET', 'test_resp3', '$', '{"a1":{"b":{"c":1}},"a2":{"b":{"c":2}}}'))
        
        r.assertEqual(r.execute_command('JSON.DEL', 'test_resp3', '$..b'), 2)
        
        # Test none existing path
        r.assertEqual(r.execute_command('JSON.DEL', 'test_resp3', '$.a1.b'), 0)

        # Test none existing key
        r.assertEqual(r.execute_command('JSON.DEL', 'test_no_such_key', '$.a1.b'), 0)

        # Test not a JSON key
        r.expect('JSON.DEL', 'test_not_JSON', '$.a1.b').raiseError()

    # Test JSON.NUMINCRBY RESP3
    def test_resp_json_num_ops(self):
        r = self.env
        r.skipOnVersionSmaller('7.0')

        r.assertTrue(r.execute_command('SET', 'test_not_JSON', 'test_not_JSON'))

        r.assertOk(r.execute_command('JSON.SET', 'test_resp3', '$', '{"a1":{"b":{"c":1}},"a2":{"b":{"c":2.2}},"a3":{"b":{"c":"val"}}}'))

        # Test NUMINCRBY
        r.assertEqual(r.execute_command('JSON.NUMINCRBY', 'test_resp3', '$.a1.b.c', 1), [2])
        r.assertEqual(r.execute_command('JSON.NUMINCRBY', 'test_resp3', '$..c', 2), [4, 4.2, None])

        # Test NUMMULTBY
        r.assertEqual(r.execute_command('JSON.NUMMULTBY', 'test_resp3', '$.a2.b.c', 2.3), [9.66])
        r.assertEqual(r.execute_command('JSON.NUMMULTBY', 'test_resp3', '$..c', 2), [8, 19.32, None])

        # Test none existing key
        r.expect('JSON.NUMINCRBY', 'test_no_such_key', '$.a1.b', '1').raiseError()

        # Test not a JSON key
        r.expect('JSON.NUMMULTBY', 'test_not_JSON', '$.a1.b', '1').raiseError()


    # Test JSON.MSET RESP3
    def test_resp_json_mset(self):
        r = self.env
        r.skipOnVersionSmaller('7.0')

        r.assertTrue(r.execute_command('SET', 'test_not_JSON', 'test_not_JSON'))

        r.assertOk(r.execute_command('JSON.MSET', 'test_resp3_1{s}', '$', '{"a1":{"b":{"c":1}},"a2":{"b":{"c":2}}}', 'test_resp3_2{s}', '$', '{"a1":{"b":{"c":1}},"a2":{"b":{"c":2}}}'))

        # Test none existing key
        r.expect('JSON.MSET', 'test_no_such_key', '$.a1.b', '1').raiseError()

        # Test not a JSON key
        r.expect('JSON.MSET', 'test_not_JSON', '$.a1.b', '1').raiseError()

    # Test JSON.MERGE RESP3
    def test_resp_json_merge(self):
        r = self.env
        r.skipOnVersionSmaller('7.0')

        r.assertTrue(r.execute_command('SET', 'test_not_JSON', 'test_not_JSON'))

        r.assertOk(r.execute_command('JSON.SET', 'test_resp3', '$', '{"a1":{"b":{"c":1}},"a2":{"b":{"c":2}}}'))

        r.assertOk(r.execute_command('JSON.MERGE', 'test_resp3', '$', '{"a3":4}'))

        # Test none existing key
        r.expect('JSON.MERGE', 'test_no_such_key', 'test_resp3_1', '$', '{"a3":4}').raiseError()

        # Test not a JSON key
        r.expect('JSON.MERGE', 'test_not_JSON', '$', '{"a3":4}').raiseError()

    # Test JSON.TYPE RESP3
    def test_resp_json_type(self):
        r = self.env
        r.skipOnVersionSmaller('7.0')
            
        r.assertTrue(r.execute_command('SET', 'test_not_JSON', 'test_not_JSON'))

        r.assertOk(r.execute_command('JSON.SET', 'test_resp3', '$', '{"a1":{"b":{"c":1}},"a2":{"b":{"c":true}}, "a4":[1.2,2,3.32], "c":null}'))

        # Test JSON.TYPE RESP3
        r.assertEqual(r.execute_command('JSON.TYPE', 'test_resp3', '$.a1.b.c'), [['integer']])
        r.assertEqual(r.execute_command('JSON.TYPE', 'test_resp3', '$..b'), [['object', 'object']])
        r.assertEqual(r.execute_command('JSON.TYPE', 'test_resp3', '$'), [['object']])
        r.assertEqual(r.execute_command('JSON.TYPE', 'test_resp3', '$.a3'), [[]])
        r.assertEqual(r.execute_command('JSON.TYPE', 'test_resp3', '$.a4'), [['array']])
        r.assertEqual(r.execute_command('JSON.TYPE', 'test_resp3', '$.a4[*]'), [['number', 'integer', 'number']])
        r.assertEqual(r.execute_command('JSON.TYPE', 'test_resp3', '$..c'), [['null', 'integer', 'boolean']])

        # Test none existing key
        r.assertEqual(r.execute_command('JSON.TYPE', 'test_no_such_key', '$.a1.b.c'), [None])

        # Test not a JSON key
        r.expect('JSON.TYPE', 'test_not_JSON', '$.a1.b.c').raiseError()
