import os

from hub_blog import app

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=os.getenv('API_PORT'),
        debug=True,
    )
