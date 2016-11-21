import sys
from ghost import Ghost

def show_error_msg(status_code, body):
    error_msg = "[{}] {} : {}".format(status_code, body['errorType'], body['message'])
    print error_msg

g = Ghost('http://localhost:2368/', '74b831ef4b2b')
status, body = g.authenticate('username@example.com', 'password')
if status != 200:
    show_error_msg(status, body)
    sys.exit(-1)

status, body = g.post('A new beginning', 'published', 'I am beginning a new life today. And I promise to make it better than before.')
if status != 201:
    show_error_msg(status, body)
    sys.exit(-2)

article_id = body['id']
status, body = g.get(article_id)
if status != 200:
    show_error_msg(status, body)
    sys.exit(-3)
print "Article url : ", body['abs_url']
print "Article body : ", body['markdown']

status, body = g.update(article_id, 'A new beginning', 'published', 'I am beginning a new life today. A life without regrets. A life full of hope.')
if status != 200:
    show_error_msg(status, body)
    sys.exit(-4)
else:
    print 'Updated article : ', article_id


status, body = g.get(article_id)
if status != 200:
    show_error_msg(status, body)
    sys.exit(-5)
print "Article url : ", body['abs_url']
print "Article body : ", body['markdown']

status = g.delete(article_id)
if status != 204:
    show_error_msg(status, body)
    sys.exit(-5)
else:
    print "Deleted article : ", article_id

status, body = g.get(article_id)
show_error_msg(status, body)
