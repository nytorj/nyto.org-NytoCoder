class TOOLS:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def RETURN_CODE(self):
        func = [{
                    "name": "return_formated_assistant_message",
                    "description": """return last assistant message to the format {'filepath','file content'}""",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "The filepath to the file to be generated, e.g. lib/main.dart"
                            },
                            "filecode": {
                                "type": "string",
                                "description": "The content of the generated file, with no instructions. Just the code."
                            }
                        },
                    }
                }
            ]

        return func

