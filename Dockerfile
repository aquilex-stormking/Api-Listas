FROM python
FROM tiangolo/uvicorn-gunicorn-fastapi
COPY . /home fast
run pip install pandas
CMD pip install BeautifulSoup
run pip install fastapi 
CMD [ "uvicorn","fast.main:app","--host","0.0.0.0","--port","8080"]