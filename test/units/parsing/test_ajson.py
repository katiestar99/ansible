# Copyright 2018, Matt Martz <matt@sivel.net>
# Copyright 2019, Andrew Klychkov @Andersson007 <aaklychkov@mail.ru>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import json

import pytest

from datetime import date, datetime
from pytz import timezone as tz

from assible.module_utils.common._collections_compat import Mapping
from assible.parsing.ajson import AssibleJSONEncoder, AssibleJSONDecoder
from assible.parsing.yaml.objects import AssibleVaultEncryptedUnicode
from assible.utils.unsafe_proxy import AssibleUnsafeText


def test_AssibleJSONDecoder_vault():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/ajson.json')) as f:
        data = json.load(f, cls=AssibleJSONDecoder)

    assert isinstance(data['password'], AssibleVaultEncryptedUnicode)
    assert isinstance(data['bar']['baz'][0]['password'], AssibleVaultEncryptedUnicode)
    assert isinstance(data['foo']['password'], AssibleVaultEncryptedUnicode)


def test_encode_decode_unsafe():
    data = {
        'key_value': AssibleUnsafeText(u'{#NOTACOMMENT#}'),
        'list': [AssibleUnsafeText(u'{#NOTACOMMENT#}')],
        'list_dict': [{'key_value': AssibleUnsafeText(u'{#NOTACOMMENT#}')}]}
    json_expected = (
        '{"key_value": {"__assible_unsafe": "{#NOTACOMMENT#}"}, '
        '"list": [{"__assible_unsafe": "{#NOTACOMMENT#}"}], '
        '"list_dict": [{"key_value": {"__assible_unsafe": "{#NOTACOMMENT#}"}}]}'
    )
    assert json.dumps(data, cls=AssibleJSONEncoder, preprocess_unsafe=True, sort_keys=True) == json_expected
    assert json.loads(json_expected, cls=AssibleJSONDecoder) == data


def vault_data():
    """
    Prepare AssibleVaultEncryptedUnicode test data for AssibleJSONEncoder.default().

    Return a list of tuples (input, expected).
    """

    with open(os.path.join(os.path.dirname(__file__), 'fixtures/ajson.json')) as f:
        data = json.load(f, cls=AssibleJSONDecoder)

    data_0 = data['password']
    data_1 = data['bar']['baz'][0]['password']

    expected_0 = (u'$ASSIBLE_VAULT;1.1;AES256\n34646264306632313333393636316'
                  '562356435376162633631326264383934326565333633366238\n3863'
                  '373264326461623132613931346165636465346337310a32643431383'
                  '0316337393263616439\n646539373134633963666338613632666334'
                  '65663730303633323534363331316164623237363831\n35363335613'
                  '93238370a313330316263373938326162386433313336613532653538'
                  '376662306435\n3339\n')

    expected_1 = (u'$ASSIBLE_VAULT;1.1;AES256\n34646264306632313333393636316'
                  '562356435376162633631326264383934326565333633366238\n3863'
                  '373264326461623132613931346165636465346337310a32643431383'
                  '0316337393263616439\n646539373134633963666338613632666334'
                  '65663730303633323534363331316164623237363831\n35363335613'
                  '93238370a313330316263373938326162386433313336613532653538'
                  '376662306435\n3338\n')

    return [
        (data_0, expected_0),
        (data_1, expected_1),
    ]


class TestAssibleJSONEncoder:

    """
    Namespace for testing AssibleJSONEncoder.
    """

    @pytest.fixture(scope='class')
    def mapping(self, request):
        """
        Returns object of Mapping mock class.

        The object is used for testing handling of Mapping objects
        in AssibleJSONEncoder.default().
        Using a plain dictionary instead is not suitable because
        it is handled by default encoder of the superclass (json.JSONEncoder).
        """

        class M(Mapping):

            """Mock mapping class."""

            def __init__(self, *args, **kwargs):
                self.__dict__.update(*args, **kwargs)

            def __getitem__(self, key):
                return self.__dict__[key]

            def __iter__(self):
                return iter(self.__dict__)

            def __len__(self):
                return len(self.__dict__)

        return M(request.param)

    @pytest.fixture
    def assible_json_encoder(self):
        """Return AssibleJSONEncoder object."""
        return AssibleJSONEncoder()

    ###############
    # Test methods:

    @pytest.mark.parametrize(
        'test_input,expected',
        [
            (datetime(2019, 5, 14, 13, 39, 38, 569047), '2019-05-14T13:39:38.569047'),
            (datetime(2019, 5, 14, 13, 47, 16, 923866), '2019-05-14T13:47:16.923866'),
            (date(2019, 5, 14), '2019-05-14'),
            (date(2020, 5, 14), '2020-05-14'),
            (datetime(2019, 6, 15, 14, 45, tzinfo=tz('UTC')), '2019-06-15T14:45:00+00:00'),
            (datetime(2019, 6, 15, 14, 45, tzinfo=tz('Europe/Helsinki')), '2019-06-15T14:45:00+01:40'),
        ]
    )
    def test_date_datetime(self, assible_json_encoder, test_input, expected):
        """
        Test for passing datetime.date or datetime.datetime objects to AssibleJSONEncoder.default().
        """
        assert assible_json_encoder.default(test_input) == expected

    @pytest.mark.parametrize(
        'mapping,expected',
        [
            ({1: 1}, {1: 1}),
            ({2: 2}, {2: 2}),
            ({1: 2}, {1: 2}),
            ({2: 1}, {2: 1}),
        ], indirect=['mapping'],
    )
    def test_mapping(self, assible_json_encoder, mapping, expected):
        """
        Test for passing Mapping object to AssibleJSONEncoder.default().
        """
        assert assible_json_encoder.default(mapping) == expected

    @pytest.mark.parametrize('test_input,expected', vault_data())
    def test_assible_json_decoder_vault(self, assible_json_encoder, test_input, expected):
        """
        Test for passing AssibleVaultEncryptedUnicode to AssibleJSONEncoder.default().
        """
        assert assible_json_encoder.default(test_input) == {'__assible_vault': expected}
        assert json.dumps(test_input, cls=AssibleJSONEncoder, preprocess_unsafe=True) == '{"__assible_vault": "%s"}' % expected.replace('\n', '\\n')

    @pytest.mark.parametrize(
        'test_input,expected',
        [
            ({1: 'first'}, {1: 'first'}),
            ({2: 'second'}, {2: 'second'}),
        ]
    )
    def test_default_encoder(self, assible_json_encoder, test_input, expected):
        """
        Test for the default encoder of AssibleJSONEncoder.default().

        If objects of different classes that are not tested above were passed,
        AssibleJSONEncoder.default() invokes 'default()' method of json.JSONEncoder superclass.
        """
        assert assible_json_encoder.default(test_input) == expected

    @pytest.mark.parametrize('test_input', [1, 1.1, 'string', [1, 2], set('set'), True, None])
    def test_default_encoder_unserializable(self, assible_json_encoder, test_input):
        """
        Test for the default encoder of AssibleJSONEncoder.default(), not serializable objects.

        It must fail with TypeError 'object is not serializable'.
        """
        with pytest.raises(TypeError):
            assible_json_encoder.default(test_input)
