from flask import Flask, abort, send_from_directory

from app.md import MdLoader, NoMdAtPath, IllegalPath
from app.markdown import Markdown
from app.ref import Refs

flask_app = Flask(__name__)
loader = MdLoader()
refs = Refs(loader)
markdown = Markdown(refs)


@flask_app.route('/')
def root():
    return send_from_directory('../static', 'index.html')


@flask_app.route('/static/<string:path>')
def serve_static(path):
    return send_from_directory('../static', path)


@flask_app.route('/<path:path>')
def serve_md(path):
    try:
        md = loader.get(path)
        return markdown.convert(md.read())
    except NoMdAtPath as err:
        print('NoMdAtPath: {}'.format(err))
        abort(404)
    except IllegalPath as err:
        print('IllegalPath: {}'.format(err))
        abort(403)


if __name__ == '__main__':
    flask_app.run(debug=True)
