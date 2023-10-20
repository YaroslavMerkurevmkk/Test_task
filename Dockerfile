FROM python:3
WORKDIR /server_project
COPY server_project/requirements.txt /server_project/requirements.txt
RUN pip install -r requirements.txt
COPY server_project/server.py /server_project/server.py
CMD [ "python3", "server.py" ]
