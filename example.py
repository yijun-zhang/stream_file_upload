
from flask import Flask,request,Request,send_file
import random

class Myrequest(Request):
    def _get_file_stream(self, total_content_length, content_type, filename=None,
                         content_length=None):
        return myfileobject(filename)

""" this is for test  a file like object"""
class myfileobject(object):
    def __init__(self, filename):
        self.filename= filename

    def seek(self, *args):
        if args[0] == 0:
            print(self.filename +" is done")

    def write(self, s):
        print(s)#do what ever you want instead of print
        return len(s)

    def read(self, *args):
        n= args[0] # number of read bytes
        if n <0 or n is None:
            return b'all content of read'
        else:
            s=b'what you want to provide'
            while len(s)<n:
                s = s+s
            if random.randint(1,21)==8:# return empty bytes to stop read
                return b''
            return s[0:n]

    def close(self):
        pass

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/upload',methods=['POST'])
def upload_file():
    data = request.files
    return " upload files has been stream processed"

@app.route('/download',methods=['GET'])
def down_file():
    filename=request.args['filename']
    fob = myfileobject(filename)
    resp = send_file(fob, attachment_filename=filename)
    resp.headers["Content-Disposition"] = "attachment;filename=" + filename + ";"
    resp.direct_passthrough = False
    return resp

if __name__ == '__main__':
    app.request_class = Myrequest
    app.run(port=8080, debug=True)
