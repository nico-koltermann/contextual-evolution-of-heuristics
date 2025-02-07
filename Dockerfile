FROM continuumio/miniconda3

ENV CONTAINER_ENABLED=True

WORKDIR /ceoh
COPY . /ceoh

RUN rm -f .env

RUN chmod +x ceoh_run_local.sh

ENV CONDA_ENV_NAME ceoh
RUN conda create --name $CONDA_ENV_NAME python=3.10 -y

COPY requirements.txt /ceoh/requirements.txt
RUN /opt/conda/bin/conda run --name $CONDA_ENV_NAME pip install --no-cache-dir -r /ceoh/requirements.txt

ENV PATH /opt/conda/envs/$CONDA_ENV_NAME/bin:$PATH
RUN echo "source activate $CONDA_ENV_NAME" >> ~/.bashrc

CMD ["bash", "-c", "/bin/bash /ceoh/ceoh_run_local.sh"]