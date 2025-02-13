from ollama import chat
from ollama import ChatResponse

class Llm:
    def __init__(self):
        pass


    def response(self, prompt):
                
        message = [
                {"role" : "system" , "content" : "you are helpful assistance provide good answer based on  prompt language"},
                {"role" : "user",  "content" : prompt}
            ]

        response : ChatResponse = chat(
                model = 'qwen:32b',
                messages= message)
            
        output = response.message.content
        # print(output)

        return output