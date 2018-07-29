from flask import Flask, abort, send_from_directory

from app.md import MdLoader, NoMdAtPath, IllegalPath
from app.markdown import markdown

flask_app = Flask(__name__)
loader = MdLoader()


@flask_app.route('/')
def root():
    return send_from_directory('../static', 'index.html')


@flask_app.route('/<path:path>')
def serve_md(path):
    try:
        md = loader.get(path)
        return markdown(md.read())
    except NoMdAtPath:
        abort(404)
    except IllegalPath:
        abort(403)


if __name__ == '__main__':
    flask_app.run(debug=True)
