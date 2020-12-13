# from wsgiref.simple_server import make_server
# from flask import Flask
#
# @app.route('/api/v1/hello-world-8')
# def hello_world():
#     return 'Hello World!'
#
# @app.route('/')
# def main():
#     return '<h1>Main<h1>'
#
# with make_server('', 8080, app) as server:
#     print("Main http://127.0.0.1:8080")
#     print("\nHello World! http://127.0.0.1:8080/api/v1/hello-world-8")
#     server.serve_forever()
#
# if __name__ == '__main__':
#     app.run()
#
# # flask