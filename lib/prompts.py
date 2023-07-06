class PROMPT:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def system(self):
        return """\
        As a versatile developer, your role is to create an intelligent AI assistant \
        capable of understanding and responding to diverse user queries. Your expertise \
        in programming and problem-solving will drive the design and implementation of \
        the assistant's conversational capabilities. You will work with various technologies, \
        select suitable programming languages, and optimize performance. Your contributions \
        will shape an adaptable and user-friendly assistant that excels in addressing user needs.
        """
    def files(self, prompt):
        return f"""\
        The user want's to develop {prompt}. Please generate a Python \
        list containing the file paths required to accomplish the query. The list should \
        represent the file paths that need to be created, accessed, or modified based on \
        the query's objective. Ensure that the paths are in the correct order and follow \
        the desired directory structure. Dont forget to add the dependencies files for the \
        application, e.g. for python projects, requirements.txt, for flutter apps, pubspec.yaml\
        , etc. Please account forany specific naming conventions \
        or patterns if applicable. Your generated list of file paths will assist in further \
        development and implementation steps related to the user query. Only return the python \
        list with the filepaths. Think exaustive about every file the user would want to create \
        and return just the ones YOU would create. Leave any comments out. Return only the python \
        list, no instructions, no comments, to be evaluated by ast.eval function.Use double quotes.
        """
    def create_files(self, path):
        return f"""\
        Now the user wants you to create the content of the file {path}. Try to return just the file content.\
        Do NOT add instructions, comments or notes.
        """
    def edit_project(self, documents, filepaths):
        return f"""\
            You are a helpful code assistant that can read, modify, edit, create, delete files on the given 
            project_structure: {filepaths}
            Usefull docs: {documents}
            Only use the factual information from the transcript to answer the question. If you are updating
            and existing project file, keep the same path. Always return the full updated code, even if you
            had make the smallest possible change to it. If you are asked to include some library, make sure
            to return the full code of the file wich the library need to be included.
        """