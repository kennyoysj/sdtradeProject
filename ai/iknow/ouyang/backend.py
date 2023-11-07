from flask import request
from appConfig import app
from controller.FileController import file_con


@app.route('/api/uploadFile', methods=['POST'])
def uplodaFile():
    if request.method == 'POST':
        return file_con.upload(request)
    return """
	    <!doctype html>
	    <title>Upload new File</title>
	    <h1>Upload new File</h1>
	    <form action="" method=post enctype=multipart/form-data>
	      <p><input type=file name=file>
	         <input type=submit value=Upload>
	    </form>
	    <p>%s</p>
	    """ % "<br>"


@app.route('/api/test', methods=['POST', "GET"])
def test():
    return file_con.test(request, need_list=["param"])
