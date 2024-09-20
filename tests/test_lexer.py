"""
test cases for lexer
"""

import json
from streamingjson import lexer


class TestCompleteJSONBase:
    """
    lexer test cases
    """

    def test_complete_json_base(self):
        """
        base test cases, will test all case in incomplete json
        """
        streaming_json_case = {
            # test case: basic object properity
            "{": "{}",  # mirror stack: [], should remove from stack: [], should push into mirror stack: ['}']
            "{}": "{}",  # mirror stack: [], should remove from stack: [], should push into mirror stack: []
            '{"': '{"":null}',  # mirror stack: ['}'], should remove from stack: [], should push into mirror stack: ['"', ':', 'n', 'u', 'l', 'l']
            '{""': '{"":null}',  # mirror stack: ['"', ':', 'n', 'u', 'l', 'l','}'], should remove from stack: ['"'], should push into mirror stack: []
            '{"a': '{"a":null}',
            '{"a"': '{"a":null}',
            '{"a":': '{"a":null}',
            '{"a":n': '{"a":null}',
            '{"a":nu': '{"a":null}',
            '{"a":nul': '{"a":null}',
            '{"a":null': '{"a":null}',
            '{"a":null , "b': '{"a":null , "b":null}',
            '{"a":t': '{"a":true}',
            '{"a":tr': '{"a":true}',
            '{"a":tru': '{"a":true}',
            '{"a":true': '{"a":true}',
            '{"a":true,': '{"a":true}',
            '{"a":true , "b': '{"a":true , "b":null}',
            '{"a":f': '{"a":false}',
            '{"a":fa': '{"a":false}',
            '{"a":fal': '{"a":false}',
            '{"a":fals': '{"a":false}',
            '{"a":false': '{"a":false}',
            '{"a":false,': '{"a":false}',
            '{"a":false , "b': '{"a":false , "b":null}',
            '{"a":-': '{"a":0}',
            '{"a":12': '{"a":12}',
            '{"a":-0': '{"a":-0}',  # @TODO: should be 0, not -0
            '{"a":-12': '{"a":-12}',
            '{"a":12,': '{"a":12}',
            '{"a":12.': '{"a":12.0}',
            '{"a":12.15': '{"a":12.15}',
            '{"a":12.15,': '{"a":12.15}',
            '{"a":-12.15,': '{"a":-12.15}',
            '{"a":-1.215e,': '{"a":-1.215}',
            '{"a":-1.215E,': '{"a":-1.215}',
            '{"a":-1.215e1,': '{"a":-1.215e1}',
            '{"a":-1.215e-1,': '{"a":-1.215e-1}',
            '{"a":-1.215e+1,': '{"a":-1.215e+1}',
            '{"a":-1.215E1,': '{"a":-1.215E1}',
            '{"a":-1.215E-1,': '{"a":-1.215E-1}',
            '{"a":-1.215E+1,': '{"a":-1.215E+1}',
            '{"a":-1.215e12': '{"a":-1.215e12}',
            '{"a":-1.215E12': '{"a":-1.215E12}',
            '{"a":-1.215e12,': '{"a":-1.215e12}',
            '{"a":-1.215E12,': '{"a":-1.215E12}',
            '{"a":"': '{"a":""}',
            '{"a":""': '{"a":""}',
            '{"a":"",': '{"a":""}',
            '{"a":"string': '{"a":"string"}',
            '{"a":"string"': '{"a":"string"}',
            '{"a":"string",': '{"a":"string"}',
            '{"a":"abcdefghijklmnopqrstuvwxyz",': '{"a":"abcdefghijklmnopqrstuvwxyz"}',
            '{"a":"ABCDEFGHIJKLMNOPQRSTUVWXYZ",': '{"a":"ABCDEFGHIJKLMNOPQRSTUVWXYZ"}',
            '{"a":"0123456789",': '{"a":"0123456789"}',
            '{"a":"https://': '{"a":"https://"}',
            '{"a":"\\u0': '{"a":""}',
            '{"a":"\\u00': '{"a":""}',
            '{"a":"\\u004': '{"a":""}',
            '{"a":"\\u0049': '{"a":"\\u0049"}',
            '{"a":"\\u0049"': '{"a":"\\u0049"}',
            '{"a":"\\u0049",': '{"a":"\\u0049"}',
            '{"a":"\\u0049","b":"': '{"a":"\\u0049","b":""}',
            '{"a":"\\u0049","b":"\\': '{"a":"\\u0049","b":""}',
            '{"a":"\\u0049","b":"\\u': '{"a":"\\u0049","b":""}',
            '{"a":"\\u0049","b":"\\u0': '{"a":"\\u0049","b":""}',
            '{"a":"\\u0049","b":"\\u00': '{"a":"\\u0049","b":""}',
            '{"a":"\\u0049","b":"\\u005': '{"a":"\\u0049","b":""}',
            '{"a":"\\u0049","b":"\\u0050': '{"a":"\\u0049","b":"\\u0050"}',
            '{"a":"\\u0049","b":"\\u0050"': '{"a":"\\u0049","b":"\\u0050"}',
            '{"a":"\\u0049","b":"\\u0050"}': '{"a":"\\u0049","b":"\\u0050"}',
            '{"a":"\\u0123",': '{"a":"\\u0123"}',
            '{"a":"\\u4567",': '{"a":"\\u4567"}',
            '{"a":"\\u89ab",': '{"a":"\\u89ab"}',
            '{"a":"\\u89AB",': '{"a":"\\u89AB"}',
            '{"a":"\\ucdef",': '{"a":"\\ucdef"}',
            '{"a":"\\ucdee",': '{"a":"\\ucdee"}',
            '{"a":"\\uaaaa",': '{"a":"\\uaaaa"}',
            '{"a":"\\uCDEF",': '{"a":"\\uCDEF"}',
            # test case: escape character
            '{"\\': '{"":null}',
            '{"\\"': '{"\\"":null}',
            '{"\\""': '{"\\"":null}',
            '{"\\"\\': '{"\\"":null}',
            '{"\\"\\""': '{"\\"\\"":null}',
            '{"\\"":': '{"\\"":null}',
            '{"a":"\\"': '{"a":"\\""}',
            '{"a":"\\""': '{"a":"\\""}',
            '{"a":"\\"\\"': '{"a":"\\"\\""}',
            '{"a":"\\"\\""': '{"a":"\\"\\""}',
            '{"a":"\\"\\"",': '{"a":"\\"\\""}',
            '{"a":"\\"\\""}': '{"a":"\\"\\""}',
            '{"\\\\': '{"\\\\":null}',
            '{"\\/': '{"\\/":null}',
            '{"\\b': '{"\\b":null}',
            '{"\\f': '{"\\f":null}',
            '{"\\n': '{"\\n":null}',
            '{"\\r': '{"\\r":null}',
            '{"\\t': '{"\\t":null}',
            '{"\\u0111': '{"\\u0111":null}',
            # test case: token in string
            '{"a":"["': '{"a":"["}',
            '{"a":"[]"': '{"a":"[]"}',
            '{"a":"]"': '{"a":"]"}',
            '{"a":"{"': '{"a":"{"}',
            '{"a":"{}"': '{"a":"{}"}',
            '{"a":"}"': '{"a":"}"}',
            '{"a":","': '{"a":","}',
            '{"a":"."': '{"a":"."}',
            '{"a":"","': '{"a":"","":null}',
            '{"a":"","b': '{"a":"","b":null}',
            '{"a":"","b"': '{"a":"","b":null}',
            '{"a":"","b":': '{"a":"","b":null}',
            '{"a":"","b":"': '{"a":"","b":""}',
            '{"a":"","b":""': '{"a":"","b":""}',
            '{"a":"","b":""}': '{"a":"","b":""}',
            '{"1': '{"1":null}',
            '{"1.': '{"1.":null}',
            '{"1.1': '{"1.1":null}',
            '{"1.10': '{"1.10":null}',
            '{"1"': '{"1":null}',
            '{"1":': '{"1":null}',
            '{"1":"': '{"1":""}',
            '{"1":"1': '{"1":"1"}',
            '{"1":"1.': '{"1":"1."}',
            '{"1":"1.1': '{"1":"1.1"}',
            '{"1":"1.10': '{"1":"1.10"}',
            '{"1":"1"': '{"1":"1"}',
            '{"1":"1"}': '{"1":"1"}',
            '{"-1":"-1"}': '{"-1":"-1"}',
            '{"t': '{"t":null}',
            '{"tr': '{"tr":null}',
            '{"tru': '{"tru":null}',
            '{"true': '{"true":null}',
            '{"true"': '{"true":null}',
            '{"true":': '{"true":null}',
            '{"true":"t': '{"true":"t"}',
            '{"true":"tr': '{"true":"tr"}',
            '{"true":"tru': '{"true":"tru"}',
            '{"true":"true': '{"true":"true"}',
            '{"true":"true"': '{"true":"true"}',
            '{"true":"true"}': '{"true":"true"}',
            '{"f': '{"f":null}',
            '{"fa': '{"fa":null}',
            '{"fal': '{"fal":null}',
            '{"fals': '{"fals":null}',
            '{"false': '{"false":null}',
            '{"false"': '{"false":null}',
            '{"false":': '{"false":null}',
            '{"false":"f': '{"false":"f"}',
            '{"false":"fa': '{"false":"fa"}',
            '{"false":"fal': '{"false":"fal"}',
            '{"false":"fals': '{"false":"fals"}',
            '{"false":"false': '{"false":"false"}',
            '{"false":"false"': '{"false":"false"}',
            '{"false":"false"}': '{"false":"false"}',
            '{"n': '{"n":null}',
            '{"nu': '{"nu":null}',
            '{"nul': '{"nul":null}',
            '{"null': '{"null":null}',
            '{"null"': '{"null":null}',
            '{"null":': '{"null":null}',
            '{"null":"n': '{"null":"n"}',
            '{"null":"nu': '{"null":"nu"}',
            '{"null":"nul': '{"null":"nul"}',
            '{"null":"null': '{"null":"null"}',
            '{"null":"null"': '{"null":"null"}',
            '{"null":"null"}': '{"null":"null"}',
            # test case: array as object value
            '{"a":[': '{"a":[]}',
            '{"a":[]': '{"a":[]}',
            '{"a":[1': '{"a":[1]}',
            '{"a":[1,': '{"a":[1]}',
            '{"a":[-0,': '{"a":[-0]}',  # @TODO: should be 0, not -0
            '{"a":[-1,': '{"a":[-1]}',
            '{"a":[1,0': '{"a":[1,0]}',
            '{"a":[1,0.0': '{"a":[1,0.0]}',
            '{"a":[1,0.01': '{"a":[1,0.01]}',
            '{"a":[1,0.01]': '{"a":[1,0.01]}',
            '{"a":[1,0.01]}': '{"a":[1,0.01]}',
            '{"a":[-1,0.01]}': '{"a":[-1,0.01]}',
            '{"a":[-1,-': '{"a":[-1,0]}',
            '{"a":[-1,-0': '{"a":[-1,-0]}',  # @TODO: should be 0, not -0
            '{"a":[1,-0.01]}': '{"a":[1,-0.01]}',
            '{"a":[-1,-0.01]}': '{"a":[-1,-0.01]}',
            '{"a":[n': '{"a":[null]}',
            '{"a":[nu': '{"a":[null]}',
            '{"a":[nul': '{"a":[null]}',
            '{"a":[null': '{"a":[null]}',
            '{"a":[null,': '{"a":[null]}',
            '{"a":[null]': '{"a":[null]}',
            '{"a":[null]}': '{"a":[null]}',
            '{"a":[t': '{"a":[true]}',
            '{"a":[tr': '{"a":[true]}',
            '{"a":[tru': '{"a":[true]}',
            '{"a":[true': '{"a":[true]}',
            '{"a":[true,': '{"a":[true]}',
            '{"a":[true]': '{"a":[true]}',
            '{"a":[true]}': '{"a":[true]}',
            '{"a":[f': '{"a":[false]}',
            '{"a":[fa': '{"a":[false]}',
            '{"a":[fal': '{"a":[false]}',
            '{"a":[fals': '{"a":[false]}',
            '{"a":[false': '{"a":[false]}',
            '{"a":[false,': '{"a":[false]}',
            '{"a":[false]': '{"a":[false]}',
            '{"a":[false]}': '{"a":[false]}',
            '{"a":["': '{"a":[""]}',
            '{"a":["b': '{"a":["b"]}',
            '{"a":["b"': '{"a":["b"]}',
            '{"a":["b",': '{"a":["b"]}',
            '{"a":["b"]': '{"a":["b"]}',
            '{"a":["b"]}': '{"a":["b"]}',
            '{"a":[{': '{"a":[{}]}',
            '{"a":[{"': '{"a":[{"":null}]}',
            '{"a":[{"b': '{"a":[{"b":null}]}',
            '{"a":[{"b"': '{"a":[{"b":null}]}',
            '{"a":[{"b":': '{"a":[{"b":null}]}',
            '{"a":[{"b":"': '{"a":[{"b":""}]}',
            '{"a":[{"b":"c': '{"a":[{"b":"c"}]}',
            '{"a":[{"b":"c"': '{"a":[{"b":"c"}]}',
            '{"a":[{"b":"c",': '{"a":[{"b":"c"}]}',
            '{"a":[{"b":"c"}': '{"a":[{"b":"c"}]}',
            '{"a":[{"b":"c"}]': '{"a":[{"b":"c"}]}',
            '{"a":[{"b":"c"}]}': '{"a":[{"b":"c"}]}',
            # test case: object as object value
            '{"a":{': '{"a":{}}',
            '{"a":{"': '{"a":{"":null}}',
            '{"a":{"b': '{"a":{"b":null}}',
            '{"a":{"b"': '{"a":{"b":null}}',
            '{"a":{"b":': '{"a":{"b":null}}',
            '{"a":{"b":"': '{"a":{"b":""}}',
            '{"a":{"b":"c': '{"a":{"b":"c"}}',
            '{"a":{"b":"c"': '{"a":{"b":"c"}}',
            '{"a":{"b":"c",': '{"a":{"b":"c"}}',
            '{"a":{"b":"c"}': '{"a":{"b":"c"}}',
            '{"a":{"b":"c"}}': '{"a":{"b":"c"}}',
            # test case: multiple object properity
            '{"a":1,"b":1.20,"c":0.03,"d":-1,"e":-1.20,"f":-0.03,"g":1.997e3,"h":-1.338e19,"i":"a","j":null,"k":true,"l":false,"m":{},"n":[]]}': '{"a":1,"b":1.20,"c":0.03,"d":-1,"e":-1.20,"f":-0.03,"g":1.997e3,"h":-1.338e19,"i":"a","j":null,"k":true,"l":false,"m":{},"n":[]]}',
            # test case: basic array element
            "[": "[]",
            "[]": "[]",
            "[n": "[null]",
            "[nu": "[null]",
            "[nul": "[null]",
            "[null": "[null]",
            "[null,": "[null]",
            "[null,null": "[null,null]",
            "[t": "[true]",
            "[tr": "[true]",
            "[tru": "[true]",
            "[true": "[true]",
            "[true,": "[true]",
            "[true,true": "[true,true]",
            "[f": "[false]",
            "[fa": "[false]",
            "[fal": "[false]",
            "[fals": "[false]",
            "[false": "[false]",
            "[false,": "[false]",
            "[false,false": "[false,false]",
            "[0": "[0]",
            "[-": "[0]",
            "[-1": "[-1]",
            "[0,": "[0]",
            "[-1,": "[-1]",
            "[-1,-": "[-1,0]",
            "[0.": "[0.0]",
            "[-0.": "[-0.0]",
            "[0.1": "[0.1]",
            "[0.12,": "[0.12]",
            "[-0.12,": "[-0.12]",
            "[1,2,": "[1,2]",
            "[1,2,0": "[1,2,0]",
            "[1,2,0.": "[1,2,0.0]",
            "[1,2,0.1": "[1,2,0.1]",
            "[1,2,0.10": "[1,2,0.10]",
            "[-1,2,0.10": "[-1,2,0.10]",
            "[-1,-2,0.10": "[-1,-2,0.10]",
            "[-1,-2,-0.10": "[-1,-2,-0.10]",
            "[1,-2,-0.10": "[1,-2,-0.10]",
            "[1,2,-0.10": "[1,2,-0.10]",
            "[1,-2,0.10": "[1,-2,0.10]",
            "[2.998e": "[2.998]",
            "[2.998E": "[2.998]",
            "[2.998e1": "[2.998e1]",
            "[2.998e-1": "[2.998e-1]",
            "[2.998e+1": "[2.998e+1]",
            "[2.998E1": "[2.998E1]",
            "[2.998E-1": "[2.998E-1]",
            "[2.998E+1": "[2.998E+1]",
            "[2.998e10": "[2.998e10]",
            "[2.998E10": "[2.998E10]",
            "[2.998e10,": "[2.998e10]",
            "[2.998E10,": "[2.998E10]",
            "[-2.998e": "[-2.998]",
            "[-2.998E": "[-2.998]",
            "[-2.998e1": "[-2.998e1]",
            "[-2.998e-1": "[-2.998e-1]",
            "[-2.998e+1": "[-2.998e+1]",
            "[-2.998E1": "[-2.998E1]",
            "[-2.998E-1": "[-2.998E-1]",
            "[-2.998E+1": "[-2.998E+1]",
            "[-2.998e10": "[-2.998e10]",
            "[-2.998E10": "[-2.998E10]",
            "[2.998e10,1": "[2.998e10,1]",
            "[2.998e10,1.0": "[2.998e10,1.0]",
            "[2.998e10,1.02": "[2.998e10,1.02]",
            "[2.998e10,1.02e": "[2.998e10,1.02]",
            "[2.998e10,1.02e8": "[2.998e10,1.02e8]",
            "[2.998E10,1.02E8": "[2.998E10,1.02E8]",
            "[2.998e10,1.02e8,": "[2.998e10,1.02e8]",
            "[2.998E10,1.02E8,": "[2.998E10,1.02E8]",
            '["': '[""]',
            '[""': '[""]',
            '["",': '[""]',
            '["a': '["a"]',
            '["a"': '["a"]',
            '["a",': '["a"]',
            '["a","': '["a",""]',
            '["a","b': '["a","b"]',
            '["a","b"': '["a","b"]',
            '["a","b",': '["a","b"]',
            '["a","b"]': '["a","b"]',
            '["\\u0': '[""]',
            '["\\u00': '[""]',
            '["\\u004': '[""]',
            '["\\u0049': '["\\u0049"]',
            '["\\u0049"': '["\\u0049"]',
            '["\\u0049",': '["\\u0049"]',
            '["\\u0049","': '["\\u0049",""]',
            '["\\u0049","\\': '["\\u0049",""]',
            '["\\u0049","\\u': '["\\u0049",""]',
            '["\\u0049","\\u0': '["\\u0049",""]',
            '["\\u0049","\\u00': '["\\u0049",""]',
            '["\\u0049","\\u005': '["\\u0049",""]',
            '["\\u0049","\\u0050': '["\\u0049","\\u0050"]',
            '["\\u0049","\\u0050"': '["\\u0049","\\u0050"]',
            '["\\u0049","\\u0050"]': '["\\u0049","\\u0050"]',
            '["\\u0123': '["\\u0123"]',
            '["\\u4567': '["\\u4567"]',
            '["\\u89ab': '["\\u89ab"]',
            '["\\u89AB': '["\\u89AB"]',
            '["\\ucdef': '["\\ucdef"]',
            '["\\uCDEF': '["\\uCDEF"]',
            # test case: object as array element
            "[{": "[{}]",
            '[{"': '[{"":null}]',
            '[{""': '[{"":null}]',
            '[{"":': '[{"":null}]',
            '[{"":"': '[{"":""}]',
            '[{"":""': '[{"":""}]',
            '[{"":""}': '[{"":""}]',
            '[{"":""}]': '[{"":""}]',
            '[{"a': '[{"a":null}]',
            '[{"a"': '[{"a":null}]',
            '[{"a":': '[{"a":null}]',
            '[{"a":"': '[{"a":""}]',
            '[{"a":"b': '[{"a":"b"}]',
            '[{"a":"b"': '[{"a":"b"}]',
            '[{"a":"b"}': '[{"a":"b"}]',
            '[{"a":"b"}]': '[{"a":"b"}]',
            '[{"a":n': '[{"a":null}]',
            '[{"a":nu': '[{"a":null}]',
            '[{"a":nul': '[{"a":null}]',
            '[{"a":null': '[{"a":null}]',
            '[{"a":null,': '[{"a":null}]',
            '[{"a":null}': '[{"a":null}]',
            '[{"a":null}]': '[{"a":null}]',
            '[{"a":t': '[{"a":true}]',
            '[{"a":tr': '[{"a":true}]',
            '[{"a":tru': '[{"a":true}]',
            '[{"a":true': '[{"a":true}]',
            '[{"a":true,': '[{"a":true}]',
            '[{"a":true}': '[{"a":true}]',
            '[{"a":true}]': '[{"a":true}]',
            '[{"a":f': '[{"a":false}]',
            '[{"a":fa': '[{"a":false}]',
            '[{"a":fal': '[{"a":false}]',
            '[{"a":fals': '[{"a":false}]',
            '[{"a":false': '[{"a":false}]',
            '[{"a":false,': '[{"a":false}]',
            '[{"a":false}': '[{"a":false}]',
            '[{"a":false}]': '[{"a":false}]',
            '[{"a":-': '[{"a":0}]',
            '[{"a":0': '[{"a":0}]',
            '[{"a":-0': '[{"a":-0}]',  # @TODO: should be 0, not -0
            '[{"a":0.': '[{"a":0.0}]',
            '[{"a":0.1': '[{"a":0.1}]',
            '[{"a":0.10': '[{"a":0.10}]',
            '[{"a":0.10,': '[{"a":0.10}]',
            '[{"a":0.10}': '[{"a":0.10}]',
            '[{"a":0.10}]': '[{"a":0.10}]',
            '[{"a":-0.10}]': '[{"a":-0.10}]',
            '[{"a":[': '[{"a":[]}]',
            '[{"a":[1': '[{"a":[1]}]',
            '[{"a":[t': '[{"a":[true]}]',
            '[{"a":[f': '[{"a":[false]}]',
            '[{"a":[n': '[{"a":[null]}]',
            '[{"a":["': '[{"a":[""]}]',
            '[{"a":[{': '[{"a":[{}]}]',
            '[{"a":[{"b":"c"},{': '[{"a":[{"b":"c"},{}]}]',
            '[{"a":[{"b":"c"},{"': '[{"a":[{"b":"c"},{"":null}]}]',
            '[{"a":[{"b":"c"},{"d"': '[{"a":[{"b":"c"},{"d":null}]}]',
            '[{"a":[{"b":"c"},{"d":-': '[{"a":[{"b":"c"},{"d":0}]}]',
            '[{"a":[{"b":"c"},{"d":-0': '[{"a":[{"b":"c"},{"d":-0}]}]',  # @TODO: should be 0, not -0
            '[{"a":[{"b":"c"},{"d":1.': '[{"a":[{"b":"c"},{"d":1.0}]}]',
            '[{"a":[{"b":"c"},{"d":1.1': '[{"a":[{"b":"c"},{"d":1.1}]}]',
            '[{"a":[{"b":"c"},{"d":-1.1': '[{"a":[{"b":"c"},{"d":-1.1}]}]',
            '[{"a":[{"b":"c"},{"d":[': '[{"a":[{"b":"c"},{"d":[]}]}]',
            '[{"a":[{"b":"c"},{"d":[{': '[{"a":[{"b":"c"},{"d":[{}]}]}]',
            # test case: multiple array element
            '[1,1.20,0.03,-1,-1.20,-0.03,1.997e3,-1.338e19,"a",null,true,false,{},[]]': '[1,1.20,0.03,-1,-1.20,-0.03,1.997e3,-1.338e19,"a",null,true,false,{},[]]',
            # test case: array as array element
            "[[": "[[]]",
            "[[]": "[[]]",
            "[[]]": "[[]]",
            "[[{": "[[{}]]",
            '[["': '[[""]]',
            '[[""': '[[""]]',
            '[["a': '[["a"]]',
            '[["a"': '[["a"]]',
            '[["a"]': '[["a"]]',
            '[["a"],': '[["a"]]',
            '[["a"],[': '[["a"],[]]',
            '[["a"],[]': '[["a"],[]]',
            '[["a"],[]]': '[["a"],[]]',
            '[["a"],{': '[["a"],{}]',
            '[["a"],{}': '[["a"],{}]',
            '[["a"],{}]': '[["a"],{}]',
            '[["a"],{"': '[["a"],{"":null}]',
            '[["a"],{"b': '[["a"],{"b":null}]',
            '[["a"],{"b"': '[["a"],{"b":null}]',
            '[["a"],{"b":': '[["a"],{"b":null}]',
            '[["a"],{"b":"': '[["a"],{"b":""}]',
            '[["a"],{"b":"c': '[["a"],{"b":"c"}]',
            '[["a"],{"b":"c"': '[["a"],{"b":"c"}]',
            '[["a"],{"b":"c"}': '[["a"],{"b":"c"}]',
            '[["a"],{"b":"c"}]': '[["a"],{"b":"c"}]',
            # test case: ignore token
            "{ }": "{ }",
            '{ " a " : -1.2 , ': '{ " a " : -1.2}',
            '{ " a " : -1.2 , "  b  "  :  " c "  ': '{ " a " : -1.2 , "  b  "  :  " c "}',
            '{ " a " : -1.2 , "  b  "  :  " c "   , "   d"  :  true  ': '{ " a " : -1.2 , "  b  "  :  " c "   , "   d"  :  true}',
            '{ " a " : -1.2 , "  b  "  :  " c "   , "   d"  :  true  , "e   "  : {  } } ': '{ " a " : -1.2 , "  b  "  :  " c "   , "   d"  :  true  , "e   "  : {  } }',
            "[ ]": "[ ]",
            "[ 1": "[ 1]",
            "[ 1 , -1.020  , true ,  false,  null": "[ 1 , -1.020  , true ,  false,  null]",
            "[ 1 , -1.020  , true ,  false,  null,  {   }": "[ 1 , -1.020  , true ,  false,  null,  {   }]",
        }
        for test_case, expect in streaming_json_case.items():
            lexer_instance = lexer.Lexer()
            err_in_append_string = lexer_instance.append_string(test_case)
            ret = lexer_instance.complete_json()
            assert err_in_append_string is None
            assert expect == ret, "unexpected JSON"

    def test_complete_json_nestad(self):
        """
        test nestad JSON by each caracter
        """
        streaming_json_content = '{"string": "这是一个字符串", "integer": 42, "float": 3.14159, "boolean_true": true, "boolean_false": false, "null": null, "object": {"empty_object": {}, "non_empty_object": {"key": "value"}, "nested_object": {"nested_key": {"sub_nested_key": "sub_nested_value"}}}, "array":["string in array", 123, 45.67, true, false, null, {"object_in_array": "object_value"},["nested_array"]]}'
        lexer_instance = lexer.Lexer()
        for char in streaming_json_content:
            err_in_append_string = lexer_instance.append_string(char)
            assert err_in_append_string is None
            ret = lexer_instance.complete_json()
            interface_for_json = None
            err_in_unmarshal = None
            try:
                interface_for_json = json.loads(ret)
            except Exception as e:
                err_in_unmarshal = e
            assert err_in_unmarshal is None

    def test_complete_json_nestad2(self):
        """
        test nestad JSON by each caracter, new line included
        """
        streaming_json_content = """{
            "string_with_escape_chars": "This string contains escape characters like \\\"quotes\\\", \\\\backslashes\\\\, \\/forwardslashes/, \\bbackspace\\b, \\fformfeed\\f, \\nnewline\\n, \\rcarriage return\\r, \\ttab\\t.",
            "scientific_notation": 2.998e8,
            "unicode_characters": "Some unicode characters: \\u0041\\u0042\\u0043\\u0044",
            "multiple_lang_strings": {
                "english": "Hello, World!",
                "chinese": "你好，世界！",
                "spanish": "¡Hola, mundo!",
                "russian": "Привет, мир!"
            },
            "json_tokens_as_strings": "{\\"key_with_invalid_token\\": \\"value_with_invalid_separator\\": \\"a\\"}",
            "nested_objects": {
                "nested_object1": {
                    "key1": "value1",
                    "key2": "value2",
                    "nested_object2": {
                        "inner_key1": "inner_value1",
                        "inner_key2": "inner_value2"
                    }
                },
                "nested_object2": {
                    "name": "John Doe",
                    "age": 30,
                    "address": {
                        "street": "123 Main St",
                        "city": "Anytown"
                    }
                }
            },
            "array_test": {
                "simple_array": [10, 20, 30, 40, 50],
                "array_of_objects": [
                    {
                        "name": "Alice",
                        "age": 25
                    },
                    {
                        "name": "Bob",
                        "age": 30
                    }
                ],
                "nested_arrays": [
                    [1, 2, 3],
                    [true, false, null]
                ],
                "empty_objects": {},
                "empty_arrays": []
            }
        }
        """
        lexer_instance = lexer.Lexer()
        for char in streaming_json_content:
            err_in_append_string = lexer_instance.append_string(char)
            assert err_in_append_string is None
            ret = lexer_instance.complete_json()
            interface_for_json = None
            err_in_unmarshal = None
            try:
                interface_for_json = json.loads(ret)
            except Exception as e:
                err_in_unmarshal = e
            assert err_in_unmarshal is None

    def test_complete_json_escape_and_etc(self):
        """
        test escape caracter and unicode
        """
        streaming_json_content = """{
      "string": "含有转义字符的字符串：\\"\\\\\\/\\b\\f\\n\\r\\t",
      "string_unicode": "含Unicode字符：\\u6211\\u662F",
      "negative_integer": -42,
      "float_scientific_notation": 6.02e23,
      "negative_float": -3.14159,
      "array_with_various_numbers": [
        0,
        -1,
        2.99792458e8,
        -6.62607015e-34
      ],
      "special_characters": "\\u003C\\u003E\\u0026\\u0027\\u0022",
      "nested_structure": {
        "nested_key_with_escaped_chars": "这是一个带有转义字符的字符串：\\\\n\\\\r\\\\t",
        "nested_object": {
          "bool_true": true,
          "bool_false": false,
          "null_value": null,
          "complex_number": 3.14e-10
        }
      }
    }
        """
        lexer_instance = lexer.Lexer()
        for char in streaming_json_content:
            err_in_append_string = lexer_instance.append_string(char)
            assert err_in_append_string is None
            ret = lexer_instance.complete_json()
            interface_for_json = None
            err_in_unmarshal = None
            try:
                interface_for_json = json.loads(ret)
            except Exception as e:
                err_in_unmarshal = e
            assert err_in_unmarshal is None
