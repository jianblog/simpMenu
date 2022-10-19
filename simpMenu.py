#coding=utf-8
##
#  Liujianbo
#  20201029
##


import io
import os, sys, json, yaml
import subprocess
from node import GroupNode, ActNode

sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)

def parseMenu(obj):
    node = None
    if type(obj) == type({}):
        if 'child' in obj:
            node = GroupNode()
            node.title = obj['title']
            node.child = parseMenu(obj['child'])
            if 'args' in obj.keys():
                node.args = obj['args']

        if 'cmd' in obj:
            node = ActNode()
            node.title= obj['title']
            node.cmd = obj['cmd']
            return node
    if type(obj) == type([]):
        node = []
        for item in obj:
            node.append(parseMenu(item))
        return node
    return node



def displayMenu(menu, selectNode):
    os.system('clear')
    print("\t\t*** ", menu.title, " ***\n")

    menuMap = {}    #页面菜单键位映射
    i = 1

    for menuItem in menu.child:
        menu_label = ''.join([str(i), '. ', menuItem.title])
        if type(menuItem) == GroupNode:
            menu_label = ''.join([menu_label, '..'])
            if menuItem.args.get('host'):
                menu_label = menu_label +'host='+menuItem.args['host']

        menuMap[str(i)] = menuItem
        i += 1
        print("\t", menu_label, "\n")

        if menuItem == selectNode:
            j = ord('a')
            children = menuItem.child
            for subItem in children:
                sub_label = ''.join([chr(j), '. ', subItem.title])
                if type(subItem) == GroupNode:
                    sub_label = ''.join([sub_label, '..'])

                menuMap[chr(j)] = subItem
                print("\t    ", sub_label, "\n")
                j += 1
    return menuMap


def makeArgs(args):
    ## 仅用于转换yml中包含的ansible-playbook特点参数
    ## --inventory hosts
    ## 传递额外参数 -e  var_files=
    argStr = []
    if args.get('inventory'):
        argStr.extend([' -i', ' ', args['inventory']])
    if args.get('keyfile'):
        argStr.extend([' --key-file', ' ', args['keyfile']])
    if args.get('var_files'):
        argStr.extend([' -e', ' ', 'var_files=', args['var_files']])
    if args.get('host'):
        argStr.extend([' -e', ' ', 'host=', args['host']])
    return ''.join(argStr)

if  __name__ == '__main__':
    abspath = os.path.dirname(os.path.realpath(sys.argv[0]))

    menu_struct = None
    menu_file = os.path.join(abspath,"menu.yml")
    if len(sys.argv) > 1 and os.path.exists(os.path.join(abspath, sys.argv[1])):
        menu_file = os.path.join(abspath, sys.argv[1])
        with open(menu_file, 'r', encoding='utf-8') as f:
            j = yaml.load(f, Loader=yaml.FullLoader)
            menu_struct = parseMenu(j)
    elif  os.path.exists(menu_file):
        with open(menu_file, 'r', encoding='utf-8') as f:
            j = yaml.load(f, Loader=yaml.FullLoader)
            menu_struct = parseMenu(j)
    elif os.path.exists(os.path.join(abspath,"menu.json")):
        menu_file = os.path.join(abspath, "menu.json")
        with open(menu_file, 'r', encoding='utf-8') as f:
            j = json.load(f)
            menu_struct = parseMenu(j)

    menu_history = []     ##历史菜单入栈
    menu_map = {}       ##按键映射
    menu_head = menu_struct
    menu_choice = None
    debug = None
    while True:
        menu_map = displayMenu(menu_head, menu_choice)
        inp = input("\n  请输入选择(r返回上级,x退出):")
        inp = inp.strip().lower()
        if inp == 'r':
            if menu_choice:
                menu_choice = None
                menu_map = displayMenu(menu_head, menu_choice)
            else:
                if len(menu_history) > 0:
                    menu_head = menu_history.pop(-1)

        if inp == 'x':
            sys.exit()

        if inp in menu_map.keys():
            if type(menu_map[inp]) == ActNode:
                print(menu_map[inp].cmd)
                shells = menu_map[inp].cmd
                k = input("\n确认执行请按y,其他返回:")
                if k != 'y':
                    continue
                ret = subprocess.Popen(shells, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dirname)
                if ret.stdout:
                    for line in ret.stdout:
                        line = line.decode('utf-8').strip()
                        print(line)
                    wait = input("\n任意键返回..")
            else:
                if inp.isdigit():
                    menu_choice = menu_map[inp]

                if inp.isalpha():
                    menu_history.append(menu_head) # 保存历史
                    menu_head = menu_choice
                    menu_choice = menu_map[inp]

        menu_map = displayMenu(menu_head, menu_choice)