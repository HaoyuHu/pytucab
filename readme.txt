清华大学研读间预约助手python版

功能：
（1）登录清华大学研读间预约系统
（2）登出清华大学研读间预约系统
（3）查询当前预约状态
（4）删除研读间预约时间
（5）修改研读间预约时间
（6）预约F2层研读间（自动寻找预约时间空闲的最佳研读间）

使用方法：
使用前请到同级目录下USERNAME_PASSWORD.txt文件中修改你的研读间预约系统账号和密码。
可将tucab.py设置为外部命令（设置方法见我的csdn博客：http://blog.csdn.net/coderhuhy/article/details/44873559）
参数如下：
-h, --help : 显示帮助
-v, --version : 显示当前清华大学研读间预约助手版本号
-a : 稍后输入用户名和密码，可以登录其他研读间预约系统帐户
-q, --query :  查询当前用户的预约状态
-d, --delete : 删除用户指定的研读间预约时间
-m, --modify : 修改用户指定的研读间预约时间, 用户可以自由设定修改后的时间
-t : 稍后输入预约日期和时间(日期格式 : 20150403, 时间格式: 09:40, 默认日期: 当前起算两天后, 即可预约的最长时限; 默认时间: 开始时间17:30, 结束时间21:30)
说明：
（1）USERNAME_PASSWORD.txt文件保存用户的账号和密码
