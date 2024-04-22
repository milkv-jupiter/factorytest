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
└── tests      # factory test case
    ├── auto   # auto test case
    └── manual # manual test case
```

## 测试项

测试项有自动测试项和手动测试项两类。自动测试项无需人工干预，自动判定测试是否通过。手动测试需要人工参与，判断是否通过。

添加测试项规则：

- 自动测试项和手动测试项分别添加到`tests/auto`和`tests/manual`目录
- 每个模块一个文件，以`test_`开头，文件里定义一个类，继承`unittest.TestCase`
- 测试项为类的方法，方法名以`test_`开头
- 类里定义一个字典`LANGUAGES`，用于支持多国语音

## 多国语言

## TODO

- 支持命令行