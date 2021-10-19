
docker build -t test_name .

docker run -d --name door_server -p 9009:80 test_name



## 建立数据库
- 首先数据库内必须有建立数据库，如n6506

## 迁移数据库
- alembic init alembic # 创建迁移文件夹
- 将alembic.ini文件中"sqlalchemy.url=..." 注释掉
- 修改alembic文件夹下env.py文件:target_metadata= Base.metadata

- alembic revision --autogenerate # 自动迁移数据库
- alembic upgrade head # 迁移文件夹