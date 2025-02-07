# Copyright (c) 2024 - Fei Liu (fliu36-c@my.cityu.edu.hk)
#
# Modified by: 
#           Thomas Bömer (thomas.bömer@tu-dortmund.de)
#           Nico Koltermann (nico.koltermann@tu-dortmund.de) 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ..llm.api_general import InterfaceAPI
from ..llm.api_local_llm import InterfaceLocalLLM

class InterfaceLLM:
    def __init__(self, api_endpoint, api_key, 
                 model_LLM, llm_use_local, llm_local_url, 
                 debug_mode, llm_temperature, llm_url_info):
        
        
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.model_LLM = model_LLM
        self.debug_mode = debug_mode
        self.llm_use_local = llm_use_local
        self.llm_local_url = llm_local_url
        self.llm_temperature = llm_temperature
        self.llm_url_info = llm_url_info

        print("- check LLM API")

        if self.llm_use_local:
            print('local llm delopyment is used ...')
            
            if self.llm_local_url == None or self.llm_local_url == 'xxx' :
                print(">> Stop with empty url for local llm !")
                exit()

            self.interface_llm = InterfaceLocalLLM(
                self.llm_local_url,
                self.model_LLM,
                self.llm_temperature,
            )

        else:
            print('remote llm api is used ...')
            print(self.model_LLM)


            if self.api_key is None or self.api_endpoint is None or self.api_key == 'xxx' or self.api_endpoint == 'xxx':
                print(">> Stop with wrong API setting: Set api_endpoint (e.g., api.chat...) and api_key (e.g., kx-...) !")
                exit()

            self.interface_llm = InterfaceAPI(
                self.api_endpoint,
                self.api_key,
                self.model_LLM,
                self.debug_mode,
                self.llm_temperature,
                self.llm_url_info
            )

            
        res = self.interface_llm.get_response("1+1=?")

        if res is None:
            print(">> Error in LLM API, wrong endpoint, key, model or local deployment!")
            exit()


    def get_response(self, prompt_content):
        response, json_data = self.interface_llm.get_response(prompt_content)

        if response is None:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("[API ERROR]: Response is None")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            return None, None

        if response == "":
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("[API ERROR]: Response is Empty")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        return response, json_data
