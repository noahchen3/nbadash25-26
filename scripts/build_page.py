"""Inline the computed data into src/template.html and write a standalone index.html."""
import sys
data, tpl, out = sys.argv[1:4]
body = open(tpl).read().replace("/*DATA*/", open(data).read().strip())
head = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n</head>\n<body>\n'
open(out, "w").write(head + body + "\n</body>\n</html>\n")
print("wrote", out)
