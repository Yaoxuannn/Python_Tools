# Python_Tools

This is a repo for tools written by Python. :)

## md2Hexo.py

This is a simple tool to format markdown for Hexo.
> Please execute this py under your _post directory for this tool will select the current directory as the default work directory
> Or you can write your _post path in the md2hexo.conf under the curDir.

This tool only support **Python 3.X**.

**If the original file starts with a h{1,2,3,4,5}, this line will be deleted automaticly.**

`V0.1 changeLog: Add exception handle.`

`V0.2 changeLog: The empty line above the first title will be ignored.`


## base.py

It's a awesome tool to help you change a .png to base64.

Help: python base.py [path1 [path2 [path3...]]][-h/--help][all]

you can specify the path for each .png or use `-all` to find all .png under the current working directory.

**The last base64 string will be pasted automatically.**

## backup.py

This is a enhanced copy tool written by python, it will generate a configure file. The sample of it has shown in this directory. The biggest feature of it is this tool can compare the file which has the same name and only the newer one will execute the copy operation. And of course, this tool run in the multi-processing mode.

## md5_file.py

Just a simple file using for calculate the md5 checksum. It has optimized a little for these BIG FILE.