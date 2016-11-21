Python class to use the Ghost JSON APIs
=========================================

Ghost Homepage : https://ghost.org/

Ghost has a REST based backend. By talking with the very helpful developer community and the chrome developer tools and going through the docs [here](http://api.ghost.org/v0.1/docs), I was able to create an interface to use the CRUD calls without interacting with the front end.

Tested on python version 2.7

Dependencies
------------

1. [Python requests library](http://docs.python-requests.org/en/master/)


Usage
-----

1. Import Ghost class from ghost file.

   `> from ghost import Ghost`

2. Initialize Ghost instance by giving the `base_url` and the `client_secret`. Client secret can be obtained by looking at the DOM of your blog.

    `> g = Ghost('http://localhost:2368', 'abcd1234')`

3. Authenticate using your username and password. This method returns a tuple of `(status_code, body)`. `status_code` is the HTTP Status code of the API call. `body` would a python `dict`. If `status_code` is `200`, then you are successfully authenticated. If not, the respose would give details about the error.

    `> status, body = g.authenticate('username@example.com', 'password)`

	Success Response
	```

	{
		"access_token": "rG7jjfqjcItYAd1v9rUNNwa3Z7IYWvLzBJvJwET6nnth1hBLW4u7hpQEJNzD6IkB6DGMDHOOBVlt36YgoXapef69nqhfDwxiYdaMA0mHW6kAw8AnHR3MVCeqoHuGqswWlbMFZk3eLH6JwvIQAD7QvwjgPnIwn1mKMN3kkrpuhzLIKLQ48DT1laugjoDHkjnHFyrUTOrLExx7laUgYhDq2xyAe0f0SVAwXJOxb6CwHK0JcUhT8dJiOFv7EG8cF3x",
		"refresh_token": "pOcBi7VtTojKWCTYw8ZaUpVbKBnpErGGr5FD6h92g1NzstghH1ViC4TLjWa3Dow67HCFVRaxBNA8pGBVbcP7ameZnuPZCjKZHNjZPvjyYvAhdeiNLy6EEj2gc8X3mnbClOkUSfhxkxhHji1vH1ZzAk1DZvafVQ8d9CphMiP5FpUYik1VrLS7V0N9ClFoG80khhBnDKy8CIlFKqryDXsIGnvHNYtVmXcKhXI0iF2MQer3RRwurN7PLbgW2acBmjt",
		"expires_in": 3600,
		"token_type": "Bearer"
	}
	```

	Error Response
	```
	{
		"message": "Your password is incorrect. <br /> 4 attempts remaining!",
		"errorType": "UnauthorizedError"
	}
	```

4. Use the CRUD operations. `post`, `get`, `update` and `delete`. Use them as follows

   a. __POST__

	` $ status, body = g.post('Title of the article', 'published', 'Text of the article in markdown/html')`

	The failure response structure would be the same as before. The success response would have this kind of structure. The `id` field is important as it would be needed to get, update and delete the article.

	Status can be one out of `draft` or `published`.

	In case of success, the `status` would be `201`.

	```
	{
		"id": 60,
		"uuid": "ba2db5cf-3155-4a08-9e0c-52e9356118b1",
		"title": "Title of the article",
		"slug": "title-of-the-article",
		"markdown": "Text of the article in markdown/html",
		"mobiledoc": null,
		"html": "<p>Text of the article in markdown/html</p>",
		"amp": null,
		"image": null,
		"featured": false,
		"page": false,
		"status": "published",
		"language": "en_US",
		"visibility": "public",
		"meta_title": null,
		"meta_description": null,
		"created_at": "2016-11-21T16:34:45.000Z",
		"created_by": 1,
		"updated_at": "2016-11-21T16:34:45.000Z",
		"updated_by": 1,
		"published_at": "2016-11-21T16:34:45.000Z",
		"published_by": 1,
		"tags": [],
		"author": 1,
		"url": "/title-of-the-article/"
	}
	```

	b. __UPDATE__

	`> status, body = g.update(60, 'New title of the article', 'published', 'Awesome new text of the article in markdown/html')`

	Success would give a `status` of `200`. Success and failure responses would be similar to the ones shown before.

	The article would be completely updated including the title and the text. So be careful.

	c. __GET__

	`> status, body = g.get(60)`

	Success would give a `status` of `200`. Success and failure responses would be similar to the ones shown before.


	d. __DELETE__

	`> status = g.delete(60)`

	Success would give a `status` of `204`. This means the article was deleted. Be careful as this is irrecoverable. It might be better to update the `status` to `draft`.




Join [this](https://ghost.org/slack/) slack channel for help. Or raise an issue here.
