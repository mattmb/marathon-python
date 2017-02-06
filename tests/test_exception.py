#!/usr/bin/env python
import mock
from marathon.exceptions import MarathonHttpError
from simplejson.scanner import JSONDecodeError


def test_marathon_http_error():
    mock_response = mock.Mock(reason='thing',
                              content=None,
                              status_code=404)
    ret = MarathonHttpError(mock_response)
    assert ret.status_code == 404
    assert ret.error_message == 'thing'


def test_marathon_http_error_content():
    mock_json = mock.Mock(return_value={'message': 'oh no',
                                        'details': 'something_bad'})
    mock_response = mock.Mock(reason='thing',
                              content=True,
                              status_code=404,
                              json=mock_json)
    ret = MarathonHttpError(mock_response)
    assert ret.error_message == 'oh no'
    assert ret.error_details == 'something_bad'

    mock_json = mock.Mock(side_effect=JSONDecodeError('BOOM', 'aaa', 2))
    mock_response = mock.Mock(reason='thing',
                              content=True,
                              status_code=404,
                              json=mock_json)
    ret = MarathonHttpError(mock_response)
