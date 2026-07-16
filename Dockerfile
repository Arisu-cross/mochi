FROM python:3.11-slim
WORKDIR /srv/mochi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# 数据默认写进 /data,部署时把持久化卷挂到这里,重启不清档
ENV MOCHI_DATA_DIR=/data
ENV PORT=8080
EXPOSE 8080
CMD ["python", "combined.py"]
