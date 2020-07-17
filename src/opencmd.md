opencmd -H(help)|O(open)|A(add)|D(delete) [name|name dir path]

opencmd -H|-h|help 打印帮助信息
eg: >opencmd -h

opencmd -O|-o|open|[NULL] name 打开name代表的指定目录|文件
eg: >opencmd hello

opencmd -A|-a|add  name dirpath 注册指定名称和目录路径
eg: >opencmd -a test d:\test

opencmd -D|-d|delete name  删除已注册的名称/目录(文件)
eg: >opencmd -d test

opencmd -OE|-oe|opene| name 打开name代表的指定目录|文件在文件浏览器
eg: >opencmd -oe hello

opencmd -v|-V|version  查看命令版本
eg: >opencmd -v