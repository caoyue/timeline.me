FROM python:3.6.1-slim
MAINTAINER caoyue

WORKDIR /app
ADD deploy/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "timeline.py"]
