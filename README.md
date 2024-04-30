工厂测试源码。

- 支持图形界面

## 依赖

- Python3
- unittest
- PyQt5

## 源码目录

```
├── cricket    # Cricket is a graphical tool that helps you run your test suites.
├── gui-main
├── res        # test case resources
├─── tests     # factory test case
│   ├── auto   # auto test case
│   └── manual # manual test case
└── utils      # common files
```

## 测试项

测试项有自动测试项和手动测试项两类。自动测试项无需人工干预，自动判定测试是否通过。手动测试需要人工参与，判断是否通过。

添加测试项规则：

- 自动测试项和手动测试项分别添加到`tests/auto`和`tests/manual`目录
- 每个模块一个文件，以`test_`开头，可以加上序号规定加载顺序，例如`test_01_`，文件里定义一个测试类，继承`unittest.TestCase`
- 测试项为类的方法，测试方法的名称必须以`test_`开头
- 类里定义一个字典`LANGUAGES`，用于支持多国语音

注意事项：

- 不要在测试方法里调用`os._exit()`、`sys.exit()`或`QApplication quit()`等方法，会导致测试中止，建议创建线程或子进程。

## 多国语言

相关文件：

- cricket/cricket/lang.py
- cricket/cricket/languages.json

语言：

- zh：中文
- en：英文

默认语言：中文，可以通过`cricket/cricket/lang.py`的_current_lang修改。

## TODO

- 支持命令行
