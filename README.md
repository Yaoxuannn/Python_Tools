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

Just a simple file using for calculate the md5 checksum. It has optimized a little for these BIG FILES.

## ProcessBar.py

This is a class that has been encapsulated. You can just download it and put into your project than use it. It is simple to use.
Just like the instruction shows:

```python
# THERE IS AN EXAMPLE
import time

a = ProcessBar()
print("Now start test.\nStage one..")
for n in range(10):
    a.update(5)
    time.sleep(0.3)

print("Second stage..")
for n in range(10):
    a.update(4)
    if n == 7:
        a.update(span=0, newline=True)
        print("[!] Error. Stop the stage two")
        break
print("The last stage...")
a.init()  # We need to reinit the processbar for the break just occured instead of the bar will continue from the breakpoint.
for n in range(5):
    a.update(5)
    time.sleep(1)
a.peek(100)
time.sleep(0.4)
a.done("Done")
```

And the effect is like:

![processbar](http://omps875vw.bkt.clouddn.com/processbar.gif)

## Fucking

This is the first tool builded by myself that has the productivity :)

Simply, this is a python tool which make English word to Chinese using the baidu translate. The feature is fucking once fetch the meaning of the word, it will save it to the local sqlite database. Then the next time you lookup the word, fucking will directly get the meaning of the word quickly from thr disk cache.

And it is easy to use:

```bash
Usage:
	 fucking word             	 Get the pronunciation and the definition of the `word`.
					(double quotation marks are needed if the `word` is a phrase or a sentence)
	 fucking -f|--force word  	 Force to fetch data from the Internet
	 fucking -u|--update word 	 Update the local cache of the `word`(Has the same effect of the -f)
	 fucking -p|--ping        	 Ping the target to check the connection
	 fucking -v|--version     	 Display the version infomation
	 fucking -h|--help        	 Print this help information
```

One example is :

```bash
~ fucking shit
From Internet:   	***shit***
美音: [ ʃɪt ]	英音: [ ʃɪt ]
释义:
	n.    ['屎，粪便', '拉屎，排便', '胡说八道', '不幸或麻烦']
	vi.   ['大便，拉屎']
	vt.   ['拉屎弄脏（某物），排便于…', '取笑', '欺骗，哄骗', '对…胡扯']
	int.   ['胡扯！放屁！讨厌！[用以表示厌恶、轻蔑、失望、愤怒等]']
~ fucking -v
fucking: 1.0.4 Written by Justin13
Bug report: justin13wyx@gmail.com
```

> How to install ?
> ```
> pip3 install fucking
> ```

changelog:

> v1.0.5: Fix bugs when in Python3.X(X <= 4) module json has different type of exception.

> v1.0.6: Add new param `-s|--size` to get the current size of the database.


Enjoy fucking !

## ascii.py

Help you quickly get the ascii code of the character.
