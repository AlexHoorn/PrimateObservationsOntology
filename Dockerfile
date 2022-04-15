FROM python:3.8
RUN pwd
WORKDIR /usr/src/app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8501
COPY app/app.py .
COPY app/pages ./pages
COPY app/config.yaml .
ENTRYPOINT ["streamlit", "run"]
CMD [ "app.py" ,"--server.address","0.0.0.0"]