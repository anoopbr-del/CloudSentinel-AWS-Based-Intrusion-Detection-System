FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install pandas numpy scikit-learn

CMD ["python","final.py"]