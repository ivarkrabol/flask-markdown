from typing import Tuple

from flask import Flask, abort, send_from_directory
from werkzeug.exceptions import NotFound

from app.md import MdLoader, NoMdAtPath, IllegalPath
from app.markdown import Markdown
from app.ref import Refs

flask_app = Flask(__name__)
loader = MdLoader()
refs = Refs(loader)
markdown = Markdown(refs)


@flask_app.route('/')
def root() -> str:
    return send_from_directory('static', 'index.html')


@flask_app.route('/<path:path>')
def serve_md(path: str) -> str:
    try:
        md = loader.get(path)
        return markdown.convert(md.read())
    except NoMdAtPath as err:
        print('NoMdAtPath: {}'.format(err))
        abort(404)
    except IllegalPath as err:
        print('IllegalPath: {}'.format(err))
        abort(403)


@flask_app.errorhandler(404)
def page_not_found(e: NotFound) -> Tuple[str, int]:
    md = loader.get('error')
    return markdown.convert(md.read(), {
        'title': '{}: {}'.format(e.code, e.name),
        'message': e.description
    }), e.code


if __name__ == '__main__':
    flask_app.run(debug=True)
