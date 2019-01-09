import os
from web.app import create_app


def runserver():
    port = int(os.environ.get('PORT', 5000))
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=port)


if __name__ == '__main__':
    runserver()
