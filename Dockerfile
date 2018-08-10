FROM python:3.7.0-slim
LABEL maintainer="caoyue"
WORKDIR /app
ADD deploy/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "timeline.py"]
