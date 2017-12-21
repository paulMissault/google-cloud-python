# Copyright 2015 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import mock


class TestConnection(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.dns._http import Connection

        return Connection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_build_api_url_no_extra_query_params(self):
        conn = self._make_one(object())
        URI = '/'.join([
            conn.API_BASE_URL,
            'dns',
            conn.API_VERSION,
            'foo',
        ])
        self.assertEqual(conn.build_api_url('/foo'), URI)

    def test_build_api_url_w_extra_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit

        conn = self._make_one(object())
        uri = conn.build_api_url('/foo', {'bar': 'baz'})
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        self.assertEqual(path,
                         '/'.join(['', 'dns', conn.API_VERSION, 'foo']))
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['bar'], 'baz')

    def test_extra_headers(self):
        import requests

        from google.cloud import _http as base_http
        from google.cloud.dns import _http as MUT

        http = mock.create_autospec(requests.Session, instance=True)
        response = requests.Response()
        response.status_code = 200
        response_data = b'brent-spiner'
        response._content = response_data
        http.request.return_value = response
        client = mock.Mock(_http=http, spec=['_http'])

        conn = self._make_one(client)
        req_data = 'req-data-boring'
        result = conn.api_request(
            'GET', '/rainbow', data=req_data, expect_json=False)
        self.assertEqual(result, response_data)

        expected_headers = {
            'Accept-Encoding': 'gzip',
            base_http.CLIENT_INFO_HEADER: MUT._CLIENT_INFO,
            'User-Agent': conn.USER_AGENT,
        }
        expected_uri = conn.build_api_url('/rainbow')
        http.request.assert_called_once_with(
            data=req_data,
            headers=expected_headers,
            method='GET',
            url=expected_uri,
        )
