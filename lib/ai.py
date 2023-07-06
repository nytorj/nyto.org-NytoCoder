import os
import sys
import time
import json
import openai
import ast
import lib.ui
import lib.openai_tools as t
import shutil
import random
import lib.prompts as pmt

import lib.config as cfg
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader

openai.api_key = "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"

embeddings = OpenAIEmbeddings()
_DELAY_REQUEST = cfg._DELAY_REQUEST
bcolors = lib.ui.BCOLORS()
tools= t.TOOLS()
return_code = tools.RETURN_CODE()
prompts = pmt.PROMPT()
model = "gpt-3.5-turbo-16k-0613"
class AI:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    def response_raw(self, msg):
        
        for delay_secs in (2**x for x in range(0, 6)):
            try:
                output = openai.ChatCompletion.create(
                        model=model,
                        temperature=0.1,
                        messages=msg,
                        stream=False
                    )
                break
            
            except openai.OpenAIError as e:
                randomness_collision_avoidance = random.randint(0, 1000) / 1000.0
                sleep_dur = delay_secs + randomness_collision_avoidance
                print(f"Error: {e}. \nRetrying in {round(sleep_dur, 2)} seconds.")
                time.sleep(sleep_dur)
                continue
        return(output['choices'][0]['message']['content'])

    def response_fnc(self, msg):
        
        for delay_secs in (2**x for x in range(0, 6)):
            try:
                output = openai.ChatCompletion.create(
                        model=model,
                        temperature = 0.1,
                        messages=msg,
                        functions=return_code,
                        function_call={"name": "return_formated_assistant_message"},
                        stream=False
                    )

                break
            
            except openai.OpenAIError as e:
                randomness_collision_avoidance = random.randint(0, 1000) / 1000.0
                sleep_dur = delay_secs + randomness_collision_avoidance
                print(f"Error: {e}. \nRetrying in {round(sleep_dur, 2)} seconds.")
                time.sleep(sleep_dur)
                continue    
        return(output['choices'][0]['message']['function_call']['arguments'])


    def write_file(self, file_path, content):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w') as file:
            file.write(str(content))
            print(f"{bcolors.FAIL}File '{bcolors.ENDC}{bcolors.WARNING}{file_path}{bcolors.ENDC}{bcolors.FAIL}' created and content{bcolors.ENDC}{bcolors.OKGREEN} written successfully.{bcolors.ENDC}")
            file.close()

    def add_messages(self, role, messages, msg_to_add):
        updated_messages = list(messages)
        if(role == "system"):
            updated_messages.append({"role": "system", "content": msg_to_add})

        if(role == "assistant"):
            updated_messages.append({"role": "system", "content": msg_to_add})

        if(role == "user"):
            updated_messages.append({"role": "system", "content": msg_to_add})
        
        return updated_messages
    
    def extract_filepath(self, str_filepaths, messages, project_name):
        updated_messages = list(messages)
        updated_messages = self.add_messages("assistant", updated_messages, str_filepaths)
        json_filepaths = json.loads(str_filepaths)
        filepaths = [path if not path.endswith("/") else os.makedirs(project_name + "/" + path[:-1]) for path in json_filepaths]
        
        return filepaths, updated_messages
    
    def extract_filecode(self, response, project_name):
        response_dict = ast.literal_eval(response)
        try:
            filecode = response_dict['filecode']
            return filecode
        except:
            return("ERROR MESSAGE:",f'Error extracting file. F{response}')
    


    def exit_program(self, message):
        print(message)
        sys.exit()

    def delete_directory(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)
        else:
            pass
    
    def output_messages_parser(self, document_content):
        content = document_content.page_content
        
        # Split the content by 'filepath:'
        sections = content.split("filepath:")[1:]  # Ignore the first item since it's empty
        
        # Extract file paths and file codes
        filecodes = []
        filepaths = []
        for section in sections:
            # Split section into file path and file code
            parts = section.split("\nfilecode:\n", 1)
            if len(parts) == 2:
                filepath, filecode = parts
                filepath = filepath.strip()
                filecode = filecode.strip()
                filecodes.append(filecode)
                filepaths.append(filepath)
        
        # Return the results
        return filecodes, filepaths
    def start(self):
    
        print(f"{bcolors.FAIL}-----------------------------------------\nWelcome to {bcolors.ENDC}{bcolors.HEADER}NytoCoder{bcolors.ENDC}.{bcolors.FAIL} Enjoy building.\n-----------------------------------------{bcolors.ENDC}")
        project_name = input(f"{bcolors.WARNING}Enter the name of your project:>{bcolors.ENDC}")
        prompt = ""
        prompt = input(f"{bcolors.OKBLUE}What do you want to build?{bcolors.ENDC}\n[{bcolors.WARNING}{project_name}{bcolors.ENDC}]:>")
        if(prompt == ""):
            with open("prompt.md", "r") as file:
                for line in file:
                    prompt+=str(line)

        print(f"\n{bcolors.FAIL}Ok, MASTER! Building...\n\n{bcolors.ENDC}{bcolors.WARNING}...{prompt}{bcolors.ENDC}")

        self.delete_directory(project_name)
        self.main(prompt, project_name, None)

        file = f"{project_name}/log.txt"
        loader = TextLoader(file)
        txt = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(txt)
        project_paths, project_codes = self.output_messages_parser(txt[0])
        
        while True:
            prompt = input(f"Anything else you want to add to your project?\n[{bcolors.WARNING}{project_name}{bcolors.ENDC}]:>")
            no_inputs = [
                "n",
                "no",
                "nah",
                "nay",
                "negative",
                "not really",
                "nope",
                "uh-uh",
                "not at all",
                "no way",
                "no thanks",
                "I don't want to add anything",
                "I'm good without any additions",
                "I'm satisfied with the project as it is",
                "I have nothing else to add",
                "I think it's complete",
                "I don't have any further suggestions",
                "I'm content with what we have",
                "I'm fine without any additional features",
                "I'm happy with the current state of the project",
                "I don't feel the need for any additions",
                "I prefer to leave it as is",
                "I'm not interested in adding anything else",
                "I'd rather not add anything",
                "I believe it's already comprehensive enough",
                "I'm not inclined to suggest any further changes",
                "I'm afraid I don't have any more inputs",
                "I'm not planning on adding anything else",
                "I'm satisfied with the project's current scope",
                "N",
                "Nah",
                "Nay",
                "Nope",
                "No way",
                "Not really",
                "Not at all"
            ]

            for no in no_inputs:
                if(str(prompt) == no):
                    self.exit_program("Ok. Good. I hope you liked the experience!")
                else:
                    pass
            
            db = FAISS.from_documents(docs, embeddings)

            docs = db.similarity_search(prompt, k=4)
            
            system_message = prompts.edit_project(docs, project_paths)

            self.main(prompt, project_name, system_message)


    def main(self, prompt, project_name,  update_sys_msg):
        messages = []
        log = ""
        system_message = update_sys_msg
        if system_message is not None:
            pass
        else:
            system_message = prompts.system()


        user_message = prompts.files(prompt=prompt)

        messages = self.add_messages("system", messages, system_message)
        messages = self.add_messages("user", messages, user_message)

        response = self.response_raw(messages)
        

        filepaths, messages = self.extract_filepath(response, messages, project_name)

        print(f"{bcolors.FAIL}\n\nFiles to be written:\n\n{bcolors.ENDC}{bcolors.WARNING}{response}{bcolors.ENDC}{bcolors.FAIL}\n\nGenerating files:\n\n{bcolors.ENDC}")

        time.sleep(_DELAY_REQUEST)
        

        for path in filepaths:
            if path is not None:
                if path.endswith("/"):
                        # Directory path
                        directory_path = os.path.join(project_name, path)
                        self.delete_directory(directory_path)
                else:
                    # File path or directory without extension
                    file_path = os.path.join(project_name, path)
                    file_name, file_ext = os.path.splitext(path)
                    
                    if file_ext == "":
                        # Directory path
                        os.makedirs(file_path)
                    else:
                        print(f"{bcolors.WARNING}-------------------------------------\n===> {path}\n-------------------------------------{bcolors.ENDC}")
                        user_message = prompts.create_files(path)
                        messages = self.add_messages("user", messages, user_message)
                        response = self.response_raw(messages)
                        messages = self.add_messages("assistant", messages, response)
                        response = self.response_fnc(messages)
                        filecode = self.extract_filecode(response, project_name)
                        print(f"\n{bcolors.OKCYAN}{filecode}{bcolors.ENDC}\n\n")
                        messages = self.add_messages("assistant", messages, response)
                        self.write_file(f"{project_name}/{path}", filecode)
                        updated_messages = [messages[0],messages[1],messages[-2],messages[-1]]
                        messages = updated_messages.copy()
                        log += f"""filepath: {file_path}\nfilecode:\n{filecode}\n\n\n"""
                        time.sleep(_DELAY_REQUEST)
            else:
                pass
        self.write_file(f"{project_name}/log.txt", log)
        time.sleep(2)
        