FROM python:3.6.9
RUN python -m pip install --upgrade pip
RUN pip install rasa-x -i https://pypi.rasa.com/simple
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 5002
ENV RASA_X_PASSWORD=meeybot2707

CMD ["rasa", "run", "actions"]
CMD ["rasa", "x", "--no-prompt"]
