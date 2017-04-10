# -*- coding: UTF-8 -*-
import sys
from blog import app


if __name__ == "__main__":
    for arg in sys.argv:
        if arg == 'runserver':
            app.run(debug=True)
