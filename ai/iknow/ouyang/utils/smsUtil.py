from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
from alibabacloud_tea_util.client import Client as UtilClient
from properties import access_key_id, access_key_secret


def create_client(access_key_id: str, access_key_secret: str, ) -> Dysmsapi20170525Client:
	"""
	使用AK&SK初始化账号Client
	:param access_key_id:
	:param access_key_secret:
	:return: Client
	:throws Exception
	"""
	config = open_api_models.Config(
		# 您的AccessKey ID,
		access_key_id=access_key_id,
		# 您的AccessKey Secret,
		access_key_secret=access_key_secret
	)
	# 访问的域名
	config.endpoint = 'dysmsapi.aliyuncs.com'
	return Dysmsapi20170525Client(config)


def send_message(
		phone_numbers, sign_name, template_code, template_param
) -> None:
	client = create_client(access_key_id, access_key_secret)
	# 1.发送短信
	send_req = dysmsapi_models.SendSmsRequest(
		phone_numbers=phone_numbers,
		sign_name=sign_name,
		template_code=template_code,
		template_param=template_param
	)
	send_resp = client.send_sms(send_req)
	code = send_resp.body.code
	if not UtilClient.equal_string(code, 'OK'):
		print(f'错误信息: {send_resp.body.message}')
