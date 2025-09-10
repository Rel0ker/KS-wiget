server {
    listen 80;
    server_name ks.dev-re.ru www.ks.dev-re.ru;

    root /var/www/ks.dev-re.ru;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # CORS headers for widget files
    location ~* \.(js|css)$ {
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type";
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location ~* \.(png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}



