"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

    * Addition
    * Subtractions
    * Multiplication
    * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
    http://localhost:8080/multiply/3/5   => 15
    http://localhost:8080/add/23/42      => 65
    http://localhost:8080/subtract/23/42 => -19
    http://localhost:8080/divide/22/11   => 2
    http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

    * Fork this repository (Session03).
    * Edit this file to meet the homework requirements.
    * Your script should be runnable using `$ python calculator.py`
    * When the script is running, I should be able to view your
        application in my browser.
    * I should also be able to see a home page (http://localhost:8080/)
        that explains how to perform calculations.
    * Commit and push your changes to your fork.
    * Submit a link to your Session03 fork repository!


"""
import traceback

result_template = """
<h1>Operation Complete!</h1>
<p>Your answer is: <strong>{result}</strong></p>
<p><a href="/">Go back to the instructions page</a></p>
"""

def bad_values_page(*args):
    page = list()
    page.append("<h2>Errors</h2>")
    page.append("<p>The following values could not be processed:</p>")
    page.append("<ul>")
    for i in args:
        page.append(f"<li>{i}</li>")
    page.append("</ul>")
    return ''.join(page)

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    sum = 0
    bad_values = list()
    for o in args:
        try:
            num = float(o)
            sum += num
        except ValueError:
            bad_values.append(o)

    page = result_template.format(result=str(sum))
    if len(bad_values) > 0:
        page += bad_values_page(bad_values)
    return page


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """

    result = 0
    first = True
    bad_values = list()
    for o in args:
        try:
            if first:
                result = float(o)
                first = False
            else:
                result -= float(o)
        except ValueError:
            bad_values.append(o)

    page = result_template.format(result=str(result))
    if len(bad_values) > 0:
        page += bad_values_page(bad_values)
    return page


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """

    result = 0
    first = True
    bad_values = list()
    for o in args:
        try:
            if first:
                result = float(o)
                first = False
            else:
                num = float(o)
                if num == 0:
                    raise ValueError
                result /= num
        except ValueError:
            bad_values.append(o)

    page = result_template.format(result=str(result))
    if len(bad_values) > 0:
        page += bad_values_page(bad_values)
    return page


def multiply(*args):
    """ Returns a STRING with the product of the arguments """

    result = 0
    first = True
    bad_values = list()
    for o in args:
        try:
            if first:
                result = float(o)
                first = False
            else:
                result *= float(o)
        except ValueError:
            bad_values.append(o)

    page = result_template.format(result=str(result))
    if len(bad_values) > 0:
        page += bad_values_page(bad_values)
    return page


def index():
  body =  ["<h1>WSGI Calculator!</h1>",
        "<p>To use this page, change the URL in the address bar. You can ",
        "add, subtract, multiply, or divide. Although you can use as many ",
        "operands as you like, you can only do one operation. eg:</p>",
        "<p>/add/5/2</p>",
        "<p>/subtract/25/42</p>",
        "<p>/multiply/0/2000</p>",
        "<p>/divide/6/2</p>"]

  return ''.join(body)


def resolve_path(path):
    funcs = {
        '': index,
        'add': add,
        'subtract': subtract,
        'divide': divide,
        'multiply': multiply
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
        body += '<a href="/">Back to the list</a>'
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Error 500 Internal Server Error</h1>"
        body += '<a href="/">Back to the list</a>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
