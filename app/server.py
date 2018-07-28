from flask import Flask, abort

from app.md import MdLoader, NoMdAtPath, IllegalPath
from app.markdown import markdown

flask_app = Flask(__name__)
loader = MdLoader()


@flask_app.route('/')
def index():
    return "<h1>Hello, World!</h1>"


@flask_app.route('/<path:path>')
def user(path):
    try:
        md = loader.get(path)
        return markdown(md.read())
    except NoMdAtPath:
        abort(404)
    except IllegalPath:
        abort(403)


if __name__ == '__main__':
    flask_app.run(debug=True)
