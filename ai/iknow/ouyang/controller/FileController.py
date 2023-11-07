from properties import *
from service.FileService import file_service
from utils.AppUtil import *


class FileController:

    def upload(self, request):
        file = request.files['file']
        model = request.form['model']
        stock = request.form['stock']
        fileName = file.filename
        if (self.allowed_file(fileName)):
            path = 'upload' + os.sep + fileName
            try:
                file.save('upload' + os.sep + fileName)
            except:
                os.mkdir('upload')
                file.save('upload' + os.sep + fileName)
            d = {'path': path, 'model': model, 'stock': stock}
            return file_service.upload(d)
        return generate_result(400, "文件格式不正确")

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @parameter_verify_without_token
    def test(self, data):
        param = data.get("param")
        return generate_result(200, param)


file_con = FileController()
