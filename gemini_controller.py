# Built in
import json

# 3RD Party Libraries
import google.generativeai as genai


# CONSTANTS
API_KEY = "AIzaSyDj5_DtF3dAcBCM5A_qIF-U8seTFWXyetg" # Gemini api key created for my account.
             # Switch to economate account later.

# This is basically a Gemini python
# wrapper with customized classes for 
# different purposes.
class GeminiController:

    # Class attributes
    api_key: str
    model: genai
    prompt: str

    # Custom constructor
    def create_controller(self):
        print("-----> Gemini controller object initialization.")
        self.api_key = API_KEY                                                # Set global API KEY, Use .env later.
        genai.configure(api_key=self.api_key)                                 # Gemini connection configuration.
        self.model = genai.GenerativeModel(model_name='gemini-1.5-flash')     # Create gemini object.
        return self                                                           # Return GeminiController instance.
    

    # Gemini OCR
    def gemini_ocr(self,
                   img_path: str):
        print("-----> Gemini controller OCR method called.")
        response: str = self.model.generate_content("Give me a random json. Do not write anything except the json.")
        print(json.loads(response.text))
        print(response.text)
        print(type(response))





inst = GeminiController()
inst.create_controller()
inst.gemini_ocr("deneme")
print(type(inst))