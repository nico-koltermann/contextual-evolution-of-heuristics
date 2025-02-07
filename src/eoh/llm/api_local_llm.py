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

import json
import logging
import requests


class InterfaceLocalLLM:
    """Language model that predicts continuation of provided source code.
    """

    def __init__(self, url, model, temperature):
        self._url = url 
        self._model = model
        self._temperature = temperature
        print(f'[LocalLLM]: {model} is used')

    def get_response(self, content: str) -> str:
        while True:
            try:
                response, full_response = self._do_request(content)
                return response, full_response
            except KeyboardInterrupt:
                print("\n[HTTP] Operation canceled by user.")
                exit(0)
            except:
                print("[HTTP] Failed, retry...")
                continue


    def _do_request(self, content: str) -> str:
        content = content.strip('\n').strip()
        # repeat the prompt for batch inference (inorder to decease the sample delay)
        data = {
            "prompt": content,
            "model": self._model,
            "stream": False,
        }

        if self._temperature is not None:
            # Range: [0.0 - 2.0], controls randomness; lower is more deterministic, higher is more creative
            data["temperature"] = self._temperature 

        headers = {'Content-Type': 'application/json'}
        response = requests.post(self._url, data=json.dumps(data), headers=headers)
        if response.status_code == 200 or response.status_code == "200":
            full_response = response.json()
            # Maybe adjust to the format of your local llm
            response = response.json()['response'] 

            return response, full_response
        else:
            logging.info(f"[HTTP-LocalAPI] ERROR CODE: {response}")
            print(f"[HTTP] ERROR CODE: {response}")
            return None, None

