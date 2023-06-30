FROM python:3.9
EXPOSE 8080
WORKDIR /app
COPY . ./

RUN pip3 install openpyxl==3.1.2 \
    numpy==1.22.0 pandas==1.3.5 plotly==5.10.0 \
    PyMySQL==1.0.2 SQLAlchemy==1.4.42 streamlit==1.20.0 \
    streamlit-aggrid==0.3.4 dash-ag-grid==2.0.0a1 \
    python-dotenv==1.0.0 mysql-connector-python==8.0.33\
    msal-streamlit-authentication==1.0.8

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8


# RUN pip3 freeze > requirements.txt
# RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080"]