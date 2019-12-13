import urllib
import re
import ast

def get_package_list():
  cur_text = str(
    urllib.request.urlopen("https://raw.githubusercontent.com/JuliaRegistries/General/master/Registry.toml").read()
  )

  cur_text = re.search(r"(?<=\[packages\]).*", cur_text).group(0)

  cur_text = cur_text.replace(" = ", " : ")
  cur_text = cur_text.replace("name", "'name'")
  cur_text = cur_text.replace("path", "'path'")

  cur_list = re.findall(r"\{[^\}]*\}", cur_text)

  cur_list = list(map(ast.literal_eval, cur_list))

  cur_list = list(sorted(map(lambda cur_item: cur_item["name"], cur_list), key=str.lower))

  return cur_list
