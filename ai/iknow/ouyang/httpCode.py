http_code = {
	'200': 'Success',  # API call has been submitted successfully
	'2002':"already created", # model data has already in database
	'400': 'Bad Request',
	'401': 'Unauthorized',  # 权限验证出错
	'403.3': '写访问被拒绝,该资源可能不属于你',
	'4003': '',
	'403': 'Forbidden',
	'404': 'Not Found',
	'500': 'Service Faild'  # 服务器端暂时无法处理请求（可能是过载或维护）or Database Query Error
}