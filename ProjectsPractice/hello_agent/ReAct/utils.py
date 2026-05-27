import json as _json


def dumps(obj, **kwargs) -> str:
    kwargs.setdefault("ensure_ascii", False)#通过setdefault方法添加参数
    return _json.dumps(obj, **kwargs)#执行
