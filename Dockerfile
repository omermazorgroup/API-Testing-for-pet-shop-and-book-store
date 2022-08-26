FROM python:3

WORKDIR /fix_API_testing

COPY . /pet_store .
COPY .gitignore .
COPY __init__.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["pytest", "./pet_store/test_pet.py"]