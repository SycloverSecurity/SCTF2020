import flask
import os
from flask import request
from flask import g
from flask import config

app = flask.Flask(__name__)
app.config['FLAG'] = 'secret'

def search(obj, max_depth):
    visited_clss = []
    visited_objs = []

    def visit(obj, path='obj', depth=0):
        yield path, obj

        if depth == max_depth:
            return

        elif isinstance(obj, (int, float, bool, str, bytes)):
            return

        elif isinstance(obj, type):
            if obj in visited_clss:
                return
            visited_clss.append(obj)
            # print(obj)

        else:
            if obj in visited_objs:
                return
            visited_objs.append(obj)

        # attributes
        for name in dir(obj):
            if name.startswith('__') and name.endswith('__'):
                if name not in ('__globals__', '__class__', '__self__',
                                '__weakref__', '__objclass__', '__module__'):
                    continue
            attr = getattr(obj, name)
            yield from visit(attr, '{}.{}'.format(path, name), depth + 1)

        # dict values
        if hasattr(obj, 'items') and callable(obj.items):
            try:
                for k, v in obj.items():
                    yield from visit(v, '{}[{}]'.format(path, repr(k)), depth)
            except:
                pass

        # items
        elif isinstance(obj, (set, list, tuple, frozenset)):
            for i, v in enumerate(obj):
                yield from visit(v, '{}[{}]'.format(path, repr(i)), depth)

    yield from visit(obj)

@app.route('/')
def index():
    return open(__file__).read()

@app.route('/shrine/<path:shrine>')
def shrine(shrine):
    with open("1.txt","w") as txt:
        for path, obj in search(request, 15):
            
            txt.write(str(path)+"\n")
            if "werkzeug.urls" in str(path):
            
                print(str(path))
                return "yes"
        # print("----------------------")
        # if str(obj) == app.config['FLAG']:
        #     return path

if __name__ == '__main__':
    app.run(debug=True)