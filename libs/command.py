from libs import loader
from libs import logger
from libs import bot as api
import config
import shlex

cmap = []
key_words = ["<ARGS>","<ALL>"]


def merge(dict_1, dict_2):
    result = dict_1.copy()
    for k, v in dict_1.items():
        if isinstance(v, dict) and k in dict_2:
            assert isinstance(dict_2[k], dict), f"For key {k}, value in dict_1 is dict, but is not in dict_2."
            merged_value = merge(dict_1[k], dict_2.pop(k))
            result[k] = merged_value
        elif k in dict_2:
            result[k] = dict_2.pop(k)
        else:
            pass
    result.update(dict_2)

    return result


def add_completer(cmd):
    com = config.custom_completer
    config.custom_completer = merge(cmd, com)


def get_completer():
    return config.custom_completer


def regCommand(*tree):
    map = p_list = {}
    for item in tree:
        if not(type(item) is tuple or callable(item)) and not type(item) is dict:
            p_list[item] = {}
            p_list = p_list[item]
    add_completer(map)
    cmap.append(list(tree))


def user_input(log, dat, bot):
    text = dat["text"]
    args = shlex.split(text)
    for c in cmap:
        if len(c) >= len(args):
            for i in range(0, len(args)):
                if args[i] != c[i]:
                    if type(c[i]) == tuple and c[i][0] in key_words:
                        pass
                    elif callable(c[i]):
                        pass
                    else:
                        break
            else:
                call_func=[]
                result=[]
                for i in range(0, len(c)):
                    if type(c[i])==tuple:
                        # <ALL> 暂时作废
                        if c[i][0]=="<ALL>":
                            result=args[i:]
                            name = c[i][1].__module__.split(".", 1)[1]
                            c[i][1](logger.getLogger(name), {"text": text, "args": args, "result": result}, api.API({}))
                            break
                        elif c[i][0]=="<ARGS>":
                            call_func.append(c[i][1])
                            result.append(args[i])
                    elif callable(c[i]):
                        name=c[i].__module__.split(".", 1)[1]
                        c[i](logger.getLogger(name),{"text":text,"args":args,"result":result},api.API({}))
                        break
                    # 魔法方法list 暂时作废
                    elif type(c[i])==list:
                        name=c[i][0].__module__.split(".", 1)[1]
                        c[i][0](logger.getLogger(name), {"text": text, "args": args, "result": result}, api.API({}))
                        break
                else:
                    for i in range(0,len(call_func)):
                        name = call_func[i].__module__.split(".", 1)[1]
                        call_func[i](logger.getLogger(name), {"text": text, "args": args, "result": result}, api.API({}))




def init_command():
    loader.regEvent("user_input", user_input)
