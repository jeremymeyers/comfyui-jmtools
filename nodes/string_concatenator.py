class StringConcatenator:
    """
    A ComfyUI node that concatenates multiple string inputs in a customizable order.
    Supports dynamic input connections and optional output reversal.
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "order": (["asc", "desc", "custom"],),
                "delimiter": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
                "reverse": ("BOOLEAN", {
                    "default": False
                }),
                "custom_sort": ("STRING", {
                    "default": "input_1, input_2",
                    "multiline": False
                }),
            },
        }
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)
    FUNCTION = "concatenate"
    CATEGORY = "string"
    
    def concatenate(self, order, delimiter, reverse, custom_sort, **kwargs):
        # Collect all input_X arguments
        inputs_dict = {}
        input_keys = []
        
        for key, value in kwargs.items():
            if key.startswith("input_"):
                inputs_dict[key] = value
                input_keys.append(key)
        
        if not inputs_dict:
            return ("No inputs provided",)
        
        # Sort based on order mode
        if order == "asc":
            # Sort numerically by input number (input_1, input_2, input_3, etc.)
            sorted_keys = sorted(input_keys, key=lambda x: int(x.split("_")[1]))
            sorted_inputs = [inputs_dict[key] for key in sorted_keys]
        
        elif order == "desc":
            # Reverse numerical sort
            sorted_keys = sorted(input_keys, key=lambda x: int(x.split("_")[1]), reverse=True)
            sorted_inputs = [inputs_dict[key] for key in sorted_keys]
        
        elif order == "custom":
            # Parse custom_sort string like "input_2, input_1, input_3"
            try:
                order_list = [item.strip() for item in custom_sort.split(",")]
                sorted_inputs = []
                for item in order_list:
                    if item in inputs_dict:
                        sorted_inputs.append(inputs_dict[item])
                    else:
                        raise ValueError(f"Unknown input name: {item}")
            except Exception as e:
                return (f"Error parsing custom sort: {str(e)}",)
        
        # Join with delimiter
        result = delimiter.join(sorted_inputs)
        
        # Reverse if enabled
        if reverse:
            result = result[::-1]
        
        return (result,)

NODE_CLASS_MAPPINGS = {
    "StringConcatenator": StringConcatenator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringConcatenator": "String Concatenator",
}# The string concatenator node
