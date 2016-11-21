import json
import requests
from urlparse import urljoin

class Ghost:
    """Class for interacting with Ghost APIs"""

    CLIENT_ID = "ghost-admin"
    GRANT_TYPE = 'password'
    AUTH_URL = "/ghost/api/v0.1/authentication/token"
    POST_URL = "/ghost/api/v0.1/posts/?include=tags"
    ARTICLE_URL = "/ghost/api/v0.1/posts/{}?include=tags"

    def __init__(self, base_url, client_secret):
        """Create a new instance with the base_url and client secret"""
        self.base_url = base_url
        self.client_secret = client_secret
        self.auth_header = None

    def authenticate(self, username, password):
        """
        Authenticate using the username and password.
        Returns (status_code, response_body).
        If successful, the status_code would be 200 (Created).
        If successful, the response contains the access token, refresh token, auth_header.
        Value of 'auth_header' field can be passed as the 'Authorization' header on in subsequent requests to the Ghost API.
        """
        if not username or not password:
            return 401, {"errors" : [{"errorType" : "Unauthorized", "message" : "Username or password is None"}]}
        url = urljoin(self.base_url, self.AUTH_URL)
        payload = {\
                'grant_type' : self.GRANT_TYPE,\
                'username' : username,\
                'password' : password,\
                'client_id' : self.CLIENT_ID,\
                'client_secret' : self.client_secret\
                }

        r = requests.post(url, data=payload)
        resp = json.loads(r.text)
        if r.status_code == 200:
            resp_body = resp
            auth_header = "{} {}".format(resp['token_type'], resp['access_token'])
            self.auth_header = auth_header
            resp['auth_header'] = auth_header
        else:
            resp_body = resp['errors'][0]
        return r.status_code, resp_body

    def post(self, title, status, text):
        """
        Post a new article using the Ghost API.
        status can be 'draft' or 'published'.
        Returns a (status_code, response_body) tuple.
        If successful, the status_code would be 201 (Created).
        If successful, the response would contain an 'id' field which would be used for getting, updating and deleting article.
        Also it would contain an 'abs_url' field which is the actual url for the article.
        """
        if self.auth_header is None:
            return 401, {"errors" : [{"errorType" : "Unauthorized", "message" : "Call authenticate method first"}]}

        url = urljoin(self.base_url, self.POST_URL)
        post = {'title' : title, 'status' : status, 'markdown' : text}
        payload = {'posts' : [post]}
        headers = {'Authorization' : self.auth_header}
        r = requests.post(url, headers=headers, json=payload)
        resp = json.loads(r.text)

        if r.status_code == 201:
            resp_body = resp['posts'][0]
            resp_body['abs_url'] = urljoin(self.base_url, resp_body['url'])
        else:
            resp_body = resp['errors'][0]
        return r.status_code, resp_body



    def update(self, article_id, title, status, text):
        """
        Updates the article of given article id using the Ghost API.
        It will always be a full update. So, the existing status and text would be overwritten.
        status can be 'draft' or 'published'.
        Returns a (status_code, response_body) tuple.
        If successful, the status_code would be 200 (OK).
        If successful, the response would also contain a 'abs_url' field which is the actual url for the article.
        """

        if self.auth_header is None:
            return 401, {"errors" : [{"errorType" : "Unauthorized", "message" : "Call authenticate method first"}]}
        if not article_id:
            return 400, {"errors" : [{"errorType" : "Bad request", "message" : "article_id is None"}]}

        url = urljoin(self.base_url, self.ARTICLE_URL.format(article_id))
        post = {'title' : title, 'status' : status, 'markdown' : text}
        payload = {'posts' : [post]}
        headers = {'Authorization' : self.auth_header}
        r = requests.put(url, headers=headers, json=payload)
        resp = json.loads(r.text)

        if r.status_code == 200:
            resp_body = resp['posts'][0]
            resp_body['abs_url'] = urljoin(self.base_url, resp_body['url'])
        else:
            resp_body = resp['errors'][0]
        return r.status_code, resp_body

    def get(self, article_id):
        """
        Get an article of given article id using the Ghost API.
        Returns a (status_code, response_body) tuple.
        If successful, the status_code would be 200 (OK).
        If successful, the response would also contain a 'abs_url' field which is the actual url for the article.
        """

        if self.auth_header is None:
            return 401, {"errors" : [{"errorType" : "Unauthorized", "message" : "Call authenticate method first"}]}
        if not article_id:
            return 400, {"errors" : [{"errorType" : "Bad request", "message" : "article_id is None"}]}

        url = self.base_url + self.ARTICLE_URL.format(article_id)
        headers = {'Authorization' : self.auth_header, 'Accept' : 'application/json'}
        r = requests.get(url, headers=headers)
        resp = json.loads(r.text)
        if r.status_code == 200:
            resp_body = resp['posts'][0]
            resp_body['abs_url'] = urljoin(self.base_url, resp_body['url'])
        else:
            resp_body = resp['errors'][0]
        return r.status_code, resp_body

    def delete(self, article_id):
        """
        Delete an article of given article id using the Ghost API.
        Be careful, the article would be lost forever,
        Returns a (status_code, response_body) tuple.
        If successful, the status_code would be 204 (No Content). This means the article is deleted.
        """
        if self.auth_header is None:
            return 401, {"errors" : [{"errorType" : "Unauthorized", "message" : "Call authenticate method first"}]}
        if not article_id:
            return 400, {"errors" : [{"errorType" : "Bad request", "message" :  "article_id is None"}]}

        url = self.base_url + self.ARTICLE_URL.format(article_id)
        headers = {'Authorization' : self.auth_header}
        r = requests.delete(url, headers=headers)
        return r.status_code

