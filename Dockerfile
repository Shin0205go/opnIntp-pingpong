FROM ubuntu:22.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git python3 python3-pip gcc cmake llvm clang

RUN pip install open-interpreter==0.1.3
RUN pip install numpy matplotlib pandas
# llamaで実行する時に必要なためインストールする
RUN pip install llama-cpp-python

ENV OPENAI_API_KEY <API_KEY>
WORKDIR /root