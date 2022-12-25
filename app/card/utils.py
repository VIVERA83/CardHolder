def get_annotations_to_str(enum_obj: type) -> str:
    """Возвращает строку из названий элементов перечисления"""
    msg = ""
    for status in enum_obj.__annotations__.keys():
        msg += f"`{status}`, "
    return msg[:-2]
