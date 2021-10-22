FROM python:alpine3.14
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps
COPY . ./

CMD ["python","Huffman_Imcr.py"]


