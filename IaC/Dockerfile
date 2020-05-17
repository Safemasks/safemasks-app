FROM python:3.7-stretch


# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
&& rm -rf /var/lib/apt/lists/*
# Custom Supervisord config

COPY ./IaC/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /usr/src/app



COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN pip install -e .


EXPOSE 80

COPY ./IaC/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
