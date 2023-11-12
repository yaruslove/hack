# FROM python:3.9.18
FROM nvcr.io/nvidia/pytorch:23.10-py3

# WORKDIR /hack/app
# COPY requirements.txt ./requirements.txt

# RUN apt update && apt install -y --no-install-recommends libgl1
# RUN pip3 install -r requirements.txt

# COPY . /app

EXPOSE 8501
EXPOSE 35800
EXPOSE 36801

# ENTRYPOINT 

# ENTRYPOINT ["streamlit","run"]  #     streamlit run streamlit-app.py --server.port

# CMD ["streamlit-app.py", "--server.port", "36800"]