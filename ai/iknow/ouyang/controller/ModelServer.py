from utils.AppUtil import parameter_verify_without_token, generate_result


class ModelServer():

    @parameter_verify_without_token
    def test(self, data):
        param = data.get("param")
        return generate_result(200, param)
