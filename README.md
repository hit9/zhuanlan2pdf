zhuanlan2pdf
------------

Port your Zhihu ZhuanLan to PDF, attempting to get offline version of
`zhanglan.zhihu.com/{some-zhuanlan-short_url_name}`

**NOTE:** All rights reserved by posts' authors and zhihu.com.

Pre-Installation
----------------

This tool requires `wkhtmltopdf`, on Ubuntu:

    sudo apt-get install wkhtmltopdf

OS Dependency
-------------

Unix like OS (OSX or Linux..)

Installation
-------------

Make sure you are on Mac or Linux and you have `wkhtmltopdf` installed.

To install this tool from GitHub:

    $ [sudo] pip install git+git://github.com/hit9/zhuanlan2pdf.git

Usage
-----

```
Usage:
  zl2pdf <name> [--pool-size=<pool-size>] [--log-level=<log-level>]
  zl2pdf [-h|-v]

Options:
  -h --help                   show help
  -v --version                show version
  --pool-size=<pool_size>     how many threads to use [default: 20]
  --log-level=<log-level>     logging level from 1 to 6, bigger to logging more [default: 5]
```

Sample Usage
-------------

```bash
$ zl2pdf happy
```

The generated PDF can be found here: https://www.dropbox.com/s/yj3bzlqudlgvmlj/happy.pdf

声明
----

知乎专栏的文章的所有权归原作者和知乎所有。若知乎网或者作者因此工具的开源发布有
权利上的意见，hit9愿停止此工具的开源。
