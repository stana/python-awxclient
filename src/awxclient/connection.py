import requests

from awxclient import exception


class ConnectionException(exception.AWXClientRequestException):
    pass


class Token_Auth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer {0.token}'.format(self)
        return request


MAX_CONNECT_ATTEMPTS = 3

class Connection(object):

    def __init__(self, base_url, verify=False):
        self.base_url = base_url 
        self.verify = verify
        if not self.verify:
            requests.packages.urllib3.disable_warnings()
        self.session = requests.Session()

    def login(self, username=None, password=None, token=None, **kwargs):
        if username and password:
            self.session.auth = (username, password)
        elif token:
            self.session.auth = Token_Auth(token)
        else:
            self.session.auth = None

    def logout(self):
        self.session.auth = None

    def request(self, relative_endpoint, method='get', json=None, data=None, query_params=None, headers=None):
        session_request_method = getattr(self.session, method, None)
        if not session_request_method:
            raise ConnectionException(message=f"Unknown request method: {method}")

        use_endpoint = relative_endpoint
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
        if use_endpoint.startswith('/'):
            use_endpoint = use_endpoint[1:]
        url = '/'.join([self.base_url, use_endpoint])

        kwargs = dict(verify=self.verify, params=query_params, json=json, data=data)

        if headers is not None:
            kwargs['headers'] = headers
        if method in ('post', 'put', 'patch', 'delete'):
            kwargs.setdefault('headers', {})['X-CSRFToken'] = self.session.cookies.get('csrftoken')
            kwargs['headers']['Referer'] = url

        for attempt in range(0, MAX_CONNECT_ATTEMPTS):
            try:
                response = session_request_method(url, **kwargs)
                break
            except requests.exceptions.ConnectionError as err:
                if attempt == MAX_CONNECT_ATTEMPTS:
                    raise err

        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            try:
                resp_content = response.json()
            except ValueError:
                resp_content = response.text
            raise exception.AWXClientRequestException(
                status=response.status_code, message=resp_content)
        except ValueError:
            return response.text

    def delete(self, relative_endpoint):
        return self.request(relative_endpoint, method='delete')

    def get(self, relative_endpoint, query_params=None, headers=None):
        return self.request(relative_endpoint, method='get', query_params=query_params, headers=headers)

    def head(self, relative_endpoint):
        return self.request(relative_endpoint, method='head')

    def options(self, relative_endpoint):
        return self.request(relative_endpoint, method='options')

    def patch(self, relative_endpoint, json=None, data=None):
        return self.request(relative_endpoint, method='patch', json=json, data=data)

    def post(self, relative_endpoint, json=None, data=None, headers=None):
        return self.request(relative_endpoint, method='post', json=json, data=data, headers=headers)

    def put(self, relative_endpoint, json=None, data=None, headers=None):
        return self.request(relative_endpoint, method='put', json=json, data=data, headers=headers)
