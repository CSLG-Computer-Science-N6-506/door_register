FROM python:3.7


RUN pip3 install passlib pydantic[email] python-jose uvicorn sqlalchemy pymysql fastapi  -i https://pypi.tuna.tsinghua.edu.cn/simple 

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"] 

