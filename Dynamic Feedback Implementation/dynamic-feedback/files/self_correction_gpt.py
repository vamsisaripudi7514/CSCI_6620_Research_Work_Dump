# import openai
# import json
# from configs.config import api, base_url, model

import json
import google.generativeai as genai
from files.internal_configs.config import google_api_key, generation_config, model_name
from files.internal_configs.extract_json import extract_json
genai.configure(api_key=google_api_key)

class GPT:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )
        self.chat_session = self.model.start_chat(history=[])

    def __call__(self, prompt, message=[]):
        combined_prompt = ""
        # for msg in message:
        #     role = msg.get("role", "").upper()
        #     content = msg.get("content", "")
        #     combined_prompt += f"{role}: {content}\n"
        num = 0
        flag = True
        combined_prompt = prompt
        while num < 3 and flag:
            try:
               response = self.chat_session.send_message(combined_prompt)
               json_response = extract_json(response.text)
               print("BLOCKER1")
               print(json_response)
            except Exception as e:
                print(e)
                continue
            try:
                json.loads(json_response)
                flag = False
            except Exception as e:
                print("BLOCKER")
                flag = True
                print(f"Attempt {num+1} failed: {e}")
                num += 1
        message.append({'role': 'assistant', 'content': json_response})

        return json_response



