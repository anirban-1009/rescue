def replace_nan(obj):
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if (
                isinstance(value, dict)
                and "$numberDouble" in value
                and value["$numberDouble"] == "NaN"
            ):
                obj[key] = ""
            else:
                replace_nan(value)
    elif isinstance(obj, list):
        for item in obj:
            replace_nan(item)
    return obj
