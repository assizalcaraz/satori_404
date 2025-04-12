FROM nginx:alpine

# Copia configuración de nginx personalizada
COPY default.conf /etc/nginx/conf.d/default.conf

# Copia los archivos de video
COPY videos/ /usr/share/nginx/html/videos/
