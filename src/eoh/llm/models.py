# Copyright (c) 2025
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


import os

###################################################################
# LLM Models for configuration of local or openrouter requests

OPENROUTER_MODELS = [
    'anthropic/claude-3.5-sonnet',
    'deepseek/deepseek-chat' # deepseek v3
]

DEEPSEEK_MODELS = [
    'deepseek-chat'
]

LOCAL_MODELS = [
    'llama3.1:70b',
    'gemma2:27b',
    'qwen2.5-coder:32b',
]

def get_model_info(model_name):

    llm_use_local = False 
    add_url_info = False 

    if model_name in LOCAL_MODELS:
        print("--- USE Local Model")
        print(f"--- > {model_name}")

        # Enter full url of your model
        llm_api_endpoint = "https://api.imi-services.imi.kit.edu/api/generate"
        llm_use_local = True
        api_key = ""

    elif model_name in OPENROUTER_MODELS:
        print("--- USE OPENROUTER Model")
        print(f"--- > {model_name}")

        api_key = os.getenv('OPENROUTER_API_KEY')
        llm_api_endpoint = "openrouter.ai"
        add_url_info="/api/v1/chat/completions"

    elif model_name in DEEPSEEK_MODELS:
        print("--- USE DEEPSEEK Model")
        print(f"--- > {model_name}")

        api_key = os.getenv('DEEPSEEK_API_KEY')
        llm_api_endpoint = "api.deepseek.com"
        add_url_info="/chat/completions"

    else:
        print("--- USE REST Model")
        print(f"--- > {model_name}")

        api_key = os.getenv('OPENAI_API_KEY')
        llm_api_endpoint = "api.openai.com"
        add_url_info="/v1/chat/completions"

    return llm_api_endpoint, add_url_info, api_key, llm_use_local