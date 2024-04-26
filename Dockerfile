FROM node:18 as build-stage

WORKDIR /app

COPY client/package*.json ./

RUN npm install

COPY client .

RUN npm run build

RUN apt-get update && apt-get install -y nginx

RUN rm -f /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

RUN mv -f dist/* /usr/share/nginx/html

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv
RUN python3 -m venv /venv

COPY server/requirements.txt .

ENV PATH="/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

COPY server .
COPY nginx/nginx.conf /etc/nginx/nginx.conf

RUN apt-get update && apt-get install -y supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["/usr/bin/supervisord"]