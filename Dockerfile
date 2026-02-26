FROM python:3

EXPOSE 1488
COPY . .
RUN python main.py

CMD ["python", "main.py"]

