FROM python:3.6

COPY . .
RUN pip install -r requirements.txt

CMD python app.py
