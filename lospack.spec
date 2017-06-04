project.name = nginx
project.version = 1.12.0
project.vendor = nginx.org
project.homepage = http://nginx.org/
project.groups = dev/sys-srv
project.description = High Performance Load Balancer, Web Server, &amp; Reverse Proxy

%build

PREFIX="{{.project__prefix}}"

cd {{.lospack__pack_dir}}/deps

if [ ! -f "nginx-1.12.0.tar.gz" ]; then
    wget http://nginx.org/download/nginx-1.12.0.tar.gz
fi
if [ -d "nginx-1.12.0" ]; then
    rm -rf nginx-1.12.0
fi
tar -zxf nginx-1.12.0.tar.gz


if [ ! -f "openssl-1.0.2k.tar.gz" ]; then
    wget https://www.openssl.org/source/openssl-1.0.2k.tar.gz
fi
if [ -d "openssl-1.0.2k" ]; then
    rm -rf openssl-1.0.2k
fi
tar -zxf openssl-1.0.2k.tar.gz


cd nginx-1.12.0
./configure \
    --user=action \
    --group=action \
    --prefix=$PREFIX \
    --sbin-path=$PREFIX/bin/nginx \
    --modules-path=$PREFIX/modules \
    --conf-path=$PREFIX/conf/nginx.conf \
    --error-log-path=$PREFIX/var/log/error.log \
    --http-log-path=$PREFIX/var/log/access.log \
    --pid-path=$PREFIX/var/run.nginx.pid \
    --lock-path=$PREFIX/var/run.nginx.lock \
    --http-client-body-temp-path=$PREFIX/var/cache/nginx/client_temp \
    --http-proxy-temp-path=$PREFIX/var/cache/nginx/proxy_temp \
    --http-fastcgi-temp-path=$PREFIX/var/cache/nginx/fastcgi_temp \
    --http-uwsgi-temp-path=$PREFIX/var/cache/nginx/uwsgi_temp \
    --http-scgi-temp-path=$PREFIX/var/cache/nginx/scgi_temp \
    --with-compat \
    --with-file-aio \
    --with-threads \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_mp4_module \
    --with-http_random_index_module \
    --with-http_realip_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-http_sub_module \
    --with-http_v2_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-stream \
    --with-stream_realip_module \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-openssl=../openssl-1.0.2k

make -j2

des_tmp=/tmp/nginx_build_tmp
mkdir -p $des_tmp
make install DESTDIR=$des_tmp

rm -rf   {{.buildroot}}/*
cp -rp   $des_tmp/$PREFIX/* {{.buildroot}}/

rm -f    {{.buildroot}}/bin/nginx.old

mkdir -p {{.buildroot}}/conf/conf.d/
mkdir -p {{.buildroot}}/modules
mkdir -p {{.buildroot}}/var/cache/{client_temp,proxy_temp,fastcgi_temp,uwsgi_temp,scgi_temp}

cd {{.lospack__pack_dir}}

install misc/nginx.conf.tpl             {{.buildroot}}/conf/nginx.conf

sed -i 's/{\[worker_processes\]}/1/g'             {{.buildroot}}/conf/nginx.conf
sed -i 's/{\[events_worker_connections\]}/8192/g' {{.buildroot}}/conf/nginx.conf
sed -i 's/{\[http_server_default_listen\]}/80/g'  {{.buildroot}}/conf/nginx.conf

cd {{.lospack__pack_dir}}/deps
rm -rf nginx-1.12.0
rm -rf openssl-1.0.2k

%files

