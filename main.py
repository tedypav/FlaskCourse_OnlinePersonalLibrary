from config import create_app
from db import db

app = create_app()


@app.before_first_request
def create_tables():
    """Create all database objects before the first request is sent."""
    db.init_app(app)
    db.create_all()


@app.after_request
def close_request(response):
    """Create any pending object if flush is used after the closing of each request."""
    db.session.commit()
    return response


if __name__ == "__main__":
    app.run()
