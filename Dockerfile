FROM python:3.9

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY parser.py .
COPY bot.py .
COPY env.py .

CMD python bot.py