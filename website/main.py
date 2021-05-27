import __init__

parent_name = '.'.join(__name__.split('.')[:-1])
print("parent ("+parent_name+") "+(__init__.__name__))

#from website.__init__ import create_app
#from flask import Flask


app = __init__.create_app()

if __name__ == '__main__':
    app.run(debug=True,port=__init__.getPort())