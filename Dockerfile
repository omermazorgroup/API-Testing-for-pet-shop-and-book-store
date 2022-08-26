FROM python:3

WORKDIR /fix_API_testing

COPY . /book_store .
COPY .gitignore .
COPY __init__.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["pytest", "./book_store/test_book.py"]