FROM jupyter/scipy-notebook

RUN mkdir my-model
ENV MODEL_DIR=/home/jovyan/my-model
ENV MODEL_FILE_LDA=clf_lda.joblib
ENV MODEL_FILE_NN=clf_nn.joblib
ENV METADATA_FILE=metadata.json

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY id_rsa ./id_rsa
COPY train.py ./train.py


