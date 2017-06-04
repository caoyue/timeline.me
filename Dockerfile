FROM python:2.7-slim
MAINTAINER caoyue

WORKDIR /app
ADD deploy/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "timeline.py"]
