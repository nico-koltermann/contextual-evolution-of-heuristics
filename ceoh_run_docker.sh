#!/bin/bash
#
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

./setup_workspace.sh

source .env 

OUTPUT_PATH=ceoh_docker_results

if [ ! -d "$OUTPUT_PATH" ]; then
    echo "Creating output directory: $OUTPUT_PATH"
    mkdir -p "$OUTPUT_PATH"
fi

docker run --rm \
    -e INSTANCES_PATH=/ceoh/instances/instances \
    -e BASE_PATH=/ceoh \
    -e EOH_PROBLEM=multibay_reshuffle \
    -e MODEL_NAME=gpt-4 \
    -e OPENAI_API_KEY=$OPENAI_API_KEY \
    -v ./$OUTPUT_PATH:/ceoh/$OUTPUT_PATH \
    -e OUTPUT_PATH=/ceoh/$OUTPUT_PATH \
    -p 11434:11434 \
    ceoh_runner

