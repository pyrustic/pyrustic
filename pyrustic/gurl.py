from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json


# Headers
_ETAG = "ETag"
_LAST_MODIFIED = "Last-Modified"
_AUTH = "Authorization"
_IF_NONE_MATCH = "If-None-Match"
_IF_MODIFIED_SINCE = "If-Modified-Since"


# HTTP Status Codes
HTTP_STATUS_CODES = {
    200: "Ok",
    201: "Created",
    301: "Moved Permanently",
    304: "Not Modified",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    422: "Unprocessable Entity"
    }


class Gurl:  # TODO write a better documentation !  ;)
    """
    Gurl is a great suite for accessing the web!
    """
    def __init__(self, token=None, headers=None,
                 web_cache=True, response_cache=True):
        """
        PARAMETERS:

        - token: Authentication token

        - headers: dict of headers. Example:
                { "Accept": "application/vnd.github.v3+json",
                  "User-Agent": "Mozilla/5.0" )

        - web_cache: bool, set it to True to activate the web cache

        - response_cache: bool, set it to True to access cached responses

        """
        self._token = token
        self._headers = {} if not headers else headers
        self._web_cache = _WebCache(response_cache) if web_cache else None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, val):
        self._token = val

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, val):
        self._headers = val

    @property
    def web_cache(self):
        if self._web_cache is None:
            return False
        return True

    @web_cache.setter
    def web_cache(self, val):
        self._web_cache = _WebCache() if val else None

    def request(self, url, body=None, method="GET", headers=None):
        """ Returns a Response object """
        headers = {} if not headers else headers
        # request object
        req = _get_req(url, body, method)
        # add request to webcache
        if self._web_cache:
            self._web_cache.add_request(url, req)
        # set authorization
        _set_authorization(req, self._token)
        # set headers
        _set_headers(req, {**self._headers, **headers})
        # get response
        response = _get_response(req)
        # add response to webcache
        if self._web_cache:
            response = self._web_cache.add_response(url, response)
        return response


class Response:
    def __init__(self, native=None, error=None, cached_response=None):
        self._native = native
        self._error = error
        self._body = None
        self._json = None
        self._text = None
        self._cached_response = cached_response

    # ========================
    #       PROPERTIES
    # ========================
    @property
    def native(self):
        return self._native

    @property
    def error(self):
        return self._error

    @property
    def error_reason(self):
        if self._error is None:
            return None
        return self._error.reason

    @property
    def code(self):
        code = None
        if self._native:
            code = self._native.getcode()
        elif isinstance(self._error, HTTPError):
            code = self._error.code
        return code

    @property
    def status(self):
        return _code_to_status(self.code)

    @property
    def reason(self):
        if self._native:
            return self._native.reason

    @property
    def headers(self):
        headers = None
        if self._native:
            headers = self._native.getheaders()
        return headers

    @property
    def url(self):
        url = None
        if self._native:
            url = self._native.geturl()
        return url

    @property
    def body(self):
        if self._body is None and self._native is not None:
            try:
                self._body = self._native.read()
            except Exception:
                pass
            except KeyboardInterrupt:
                pass
        return self._body

    @property
    def json(self):
        if self._json is None:
            data = _decode_data(self.body)
            self._json = _load_json(data)
        return self._json

    @property
    def cached_response(self):
        return self._cached_response

    # ========================
    #         PUBLIC
    # ========================
    def show(self, include_headers=False, include_body=False):
        if self._text is not None:
            return self._text
        texts = []
        # ERROR
        if self._error is not None:
            cache = "ERROR: {}".format(self._error.reason)
            texts.append(cache)
        # STATUS
        status = self.code
        if status is not None:
            cache = "STATUS: {}".format(status)
            texts.append(cache)
        # URL
        url = self.url
        if url is not None:
            cache = "URL: {}".format(url)
            texts.append(cache)
        if self._native is not None:
            # REASON
            cache = "REASON: {}".format(self._native.reason)
            texts.append(cache)
            # HEADERS
            if include_headers:
                headers_text = "\n".join("{}: {}".format(x, y)
                                         for x, y in self._native.getheaders())
                cache = "HEADERS:\n{}".format(headers_text)
                texts.append(cache)
            # BODY
            if include_body:
                data = _decode_data(self.body)
                cache = "BODY:\n{}".format(data)
                texts.append(cache)
        self._text = "\n".join(texts)
        return self._text

    def header(self, name, default=None):
        if self._native:
            return self._native.getheader(name, default)
        return default


def dict_to_json_body(data):
    data = json.dumps(data)
    return data.encode()

# ========================
#       PRIVATE
# ========================


def _get_req(url, body, method):
    req = Request(url, data=body, method=method)
    return req


def _set_authorization(req, token):
    # authorization
    if token:
        req.add_header(_AUTH, "token {}".format(token))


def _set_headers(req, headers):
    # add headers
    for key, val in headers.items():
        req.add_header(key, val)


def _get_response(req):
    """ Returns a Response object """
    error = response = None
    try:
        response = urlopen(req)
    except HTTPError as e:
        error = e
    except URLError as e:
        error = e
    except Exception as e:
        error = e
    except KeyboardInterrupt:
        pass
    return Response(native=response, error=error)


def _decode_data(data, encoding="utf-8"):
    try:
        data = data.decode(encoding)
    except Exception as e:
        data = None
    except KeyboardInterrupt:
        pass
    return data


def _load_json(text):
    try:
        text = json.loads(text)
    except Exception as e:
        text = None
    except KeyboardInterrupt:
        pass
    return text


def _code_to_status(code):
    text = None
    if code is None:
        text = "Check your connection"
    else:
        text = HTTP_STATUS_CODES.get(code, "Unknown HTTP Status Code")
    return code, text


class _WebCache:
    #  TODO: what happens when you make a request 1, the server doesn't return
    # a body. You do a request 2, the server states you that the resources
    # hasn't changed, so technically you can count on the cached_response.
    # but... the cached_response doesn't have a body (there aren't even a cached response !)

    def __init__(self, cache_response):
        self._response_cache = {} if cache_response else None
        self._cache = {}

    def add_request(self, url, req):
        if url in self._cache:
            validator, value = self._cache[url]
            header = _IF_NONE_MATCH
            if validator == _LAST_MODIFIED:
                header = _IF_MODIFIED_SINCE
            headers = {header: value}
            _set_headers(req, headers)

    def add_response(self, url, response):
        etag_header = response.header(_ETAG, None)
        last_modified_header = response.header(_LAST_MODIFIED, None)
        if etag_header is not None:
            self._cache[url] = (_ETAG, etag_header)
        elif last_modified_header is not None:
            self._cache[url] = (_LAST_MODIFIED, last_modified_header)
        return self._get_response(url, response)

    def _get_response(self, url, response):
        if self._response_cache is None:
            pass
        elif response.code == 304:
            response = Response(native=response.native,
                                error=response.error,
                                cached_response=self._response_cache.get(url, None))
        elif response.body:
            self._response_cache[url] = response
        # TODO, what if response.body is None ? No cached_response. But next
        # request will state that resource hasn't changed... so it won't send any body !
        return response
