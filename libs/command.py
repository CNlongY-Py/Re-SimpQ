from libs import loader
import config
import shlex

cmap = []
key_words = [None, "<ARGS>", "<STR>", "<INT>", "<FLOAT>", "<ALL>"]


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
        if item not in key_words and not type(item) is dict:
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
                if args[i] != c[i] and c[i] not in key_words:
                    break
            else:
                log.info(c)
                log.info(args)


def init_command():
    loader.regEvent("user_input", user_input)
