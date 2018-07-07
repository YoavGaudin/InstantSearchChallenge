import webtest
from unittest import TestCase
import main


class TestGetHandler(TestCase):
    def setUp(self):
        pass

    def test_get(self):
        app = webtest.TestApp(main.application)

        response = app.get('/get')

        assert response.status_int == 200
        assert response.body == 'GetHandler'


class TestRequestSequence(TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.application)

    def _test_sequence(self, sequence):
        for cmd, params, expected in sequence:
            response = self.app.get('/{}'.format(cmd), params)
            self.assertEqual(response, expected)

    def test_sequence_1(self):
        seq = [
            ('set', {'name': 'ex', 'value': 10}, ''),
            ('get', {'name': 'ex'}, '10'),
            ('unset', {'name': 'ex'}, ''),
            ('get', {'name': 'ex'}, None),
            ('end', {}, ''),
        ]
        self._test_sequence(seq)

    def test_sequence_2(self):
        seq = [
            ('set', {'name': 'a', 'value': 10}, ''),
            ('set', {'name': 'b', 'value': 10}, ''),
            ('numequalto', {'value': 10}, '2'),
            ('numequalto', {'value': 20}, '0'),
            ('set', {'name': 'b', 'value': 30}, ''),
            ('numequalto', {'value': 10}, '1'),
            ('end', {}, ''),
            ('get', {'name': 'a'}, None),
            ('get', {'name': 'b'}, None),
        ]
        self._test_sequence(seq)

    def test_sequence_3(self):
        seq = [
            ('set', {'name': 'a', 'value': 10}, ''),
            ('set', {'name': 'b', 'value': 20}, ''),
            ('get', {'name': 'a'}, '10'),
            ('get', {'name': 'b'}, '20'),
            ('undo', {}, ''),
            ('get', {'name': 'a'}, '10'),
            ('get', {'name': 'b'}, None),
            ('set', {'name': 'a', 'value': 40}, ''),
            ('get', {'name': 'a'}, '40'),
            ('undo', {}, ''),
            ('get', {'name': 'a'}, '10'),
            ('undo', {}, ''),
            ('get', {'name': 'a'}, None),
            ('undo', {}, 'NO COMMANDS'),
            ('end', {}, ''),
        ]
        self._test_sequence(seq)



