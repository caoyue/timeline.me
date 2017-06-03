FROM python:2.7-slim
MAINTAINER caoyue

WORKDIR /app
ADD . /app
RUN pip install -r deploy/requirements.txt
EXPOSE 80
CMD ["python", "timeline.py"]
