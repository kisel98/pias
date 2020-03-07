from . import app
from . import views
from . import database
import os
from .api import __init__

app.config['SECRET_KEY'] = os.urandom(8)

if __name__ == "__main__":
    app.run()
