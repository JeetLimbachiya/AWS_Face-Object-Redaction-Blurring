FROM ubuntu:18.04
RUN apt-get update && apt-get install python3-pip -y
RUN apt-get install -y curl jq
RUN curl -LO "http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh"
RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda
RUN mkdir -p /root/FaceBlurring
COPY requirements.txt ./root/FaceBlurring/
RUN conda install python==3.9.0
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install -r ./root/FaceBlurring/requirements.txt
RUN apt-get install ffmpeg libsm6 libxext6  -y
ENV HOME /root/
COPY  Faceblurring.py \

      upload_file_to_S3.py \

      Students_1.mp4 ./root/FaceBlurring/



