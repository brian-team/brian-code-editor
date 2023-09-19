import ast

code = "hello"

parsed_code = ast.parse(code)


print(parsed_code.body[0].id)