from typing import Tuple

from flask import Flask, abort, send_from_directory
from werkzeug.exceptions import NotFound

from flaskmarkdown.app.md import MdLoader, NoMdAtPath, IllegalPath
from flaskmarkdown.app.markdown import Markdown
from flaskmarkdown.app.ref import Refs


def create_app():
    app = Flask(__name__)
    loader = MdLoader()
    refs = Refs(loader)
    markdown = Markdown(refs)

    @app.route('/')
    def root() -> str:
        return send_from_directory('static', 'index.html')

    @app.route('/<path:path>')
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

    @app.errorhandler(404)
    def page_not_found(e: NotFound) -> Tuple[str, int]:
        md = loader.get('error')
        return markdown.convert(md.read(), {
            'title': '{}: {}'.format(e.code, e.name),
            'message': e.description
        }), e.code

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
