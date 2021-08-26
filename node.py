#coding=utf-8


class Node(object):
    def __init__(self):
        self.__title = None
        self.__child = []
        self.__next = None

    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def child(self):
        return self.__child
    @child.setter
    def child(self, ndlist):
        self.__child = ndlist

    def addChild(self, nd):
        self.__child.append(nd)


class GroupNode(Node):
    # 子类 group:
    def __init__(self):
        super(GroupNode, self).__init__()
        self.__hostgroup = None
        self.__args = {}

    @property
    def hostgroup(self):
        return self.__hostgroup
    @hostgroup.setter
    def hostgroup(self, name):
        self.__hostgroup = name

    @property
    def args(self):
        return self.__args
    @args.setter
    def args(self, args):
        self.__args = args


class ActNode(GroupNode):
    # 执行子类
    def __init__(self):
        super(ActNode, self).__init__()
        self.__cmd = None

    @property
    def cmd(self):
        return self.__cmd
    @cmd.setter
    def cmd(self, cmd):
        self.__cmd = cmd

    def addCmd(self, part):
        self.__cmd.append(part)