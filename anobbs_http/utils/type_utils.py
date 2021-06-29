__all__ = [
    "TypeChecker"
]


class TypeChecker:
    ANY = "{i/H/m9R-HKES(~i*FeH|]c|,9D-cNoE"
    INT_STR = "!?Hp+dM=%Q$)n'4;=OfJ){CK{QbuINh{"

    def __init__(self, template):
        self.__temp = template

    def check(self, instance) -> None:
        def dict_type_check(json_template, json_instance, key_path="obj") -> bool:
            if json_template == self.ANY:
                return True
            elif json_template == self.INT_STR:
                if isinstance(json_instance, int) or isinstance(json_instance, str):
                    return True
                else:
                    raise RuntimeError(f"{json_instance} should be int or str")

            if type(json_template) != type(json_instance):
                now_type = type(json_instance).__name__
                should_type = type(json_template).__name__
                raise RuntimeError(f"Type not same: {key_path} should be '{should_type}' but not '{now_type}'")

            if type(json_template) == dict:
                # Support more keys
                # if set(json_instance.keys()) != set(json_template_inside.keys()):
                #     raise RuntimeError(
                #         f"JSON key error:{sorted(json_instance.keys())} != {sorted(json_template_inside.keys())}")
                for template_key, template_item in json_template.items():
                    dict_type_check(template_item, json_instance.get(template_key), f"{key_path}.{template_key}")
                return True
            elif type(json_template) == list:
                if not json_template:
                    template_item = self.ANY
                else:
                    template_item = json_template[0]

                for index, instance_item in enumerate(json_instance):
                    dict_type_check(template_item, instance_item, f"{key_path}.{index}")
                return True
            else:
                return True

        dict_type_check(self.__temp, instance)

    def chack_without_raise(self, instance) -> bool:
        try:
            self.check(instance)
            return True
        except RuntimeError:
            return False
