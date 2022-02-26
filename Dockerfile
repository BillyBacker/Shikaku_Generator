FROM python:3.8

COPY . /src

EXPOSE 9001:9001

RUN pip install fastapi
RUN pip install uvicorn
RUN pip install requests

CMD ["python", "src/main.py"]