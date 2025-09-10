server {
    listen 80;
    server_name front.ks.dev-re.ru;

    root /var/www/front.ks.dev-re.ru;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}



