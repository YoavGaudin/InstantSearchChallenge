import requests
import time


class TestRequestSequence():
    def run_tests(self):
        print("Running test 1")
        self.test_sequence_1()
        print("Running test 2")
        self.test_sequence_2()
        print("Running test 3")
        self.test_sequence_3()

    @staticmethod
    def get(cmd, params):
        url = 'https://instantsearchchallenge.appspot.com{}'.format(cmd)
        return requests.get(url, params=params)

    def _test_sequence(self, sequence):
        for cmd, params, expected in sequence:
            response = self.get('/{}'.format(cmd), params)
            try:
                assert response.content == str(expected)
            except AssertionError as e:
                self.get('/end', {})
                raise e
            print("\t{} {} returned '{}' == '{}'".format(cmd, params, response.content, expected))
            time.sleep(1)

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


if __name__ == '__main__':
    TestRequestSequence().run_tests()