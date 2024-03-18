#!/usr/bin/env bash
#
# Copyright (C) 2024 Intel Corporation.
#
# SPDX-License-Identifier: Apache-2.0
#

export PYTHONUNBUFFERED=1
socket_folder=\${XPUM_SOCKET_FOLDER:-/tmp}
rest_host=\${XPUM_REST_HOST:-0.0.0.0}
rest_port=\${XPUM_REST_PORT:-29999}
rest_no_tls=\${XPUM_REST_NO_TLS:-0}
/usr/bin/xpumd -s \${socket_folder} &
until [ -e \${socket_folder}/xpum_p.sock ]; do sleep 0.1; done

if [ \"\${rest_no_tls}\" != \"1\" ]
then
  rest_tls_param=\"--certfile conf/cert.pem --keyfile conf/key.pem\"
fi

cd /usr/lib/xpum/rest && exec gunicorn \${rest_tls_param} --bind \${rest_host}:\${rest_port} --worker-class gthread --threads 10 --worker-connections 1000 -w 1 'xpum_rest_main:main()' &

xpumcli dump --rawdata --start -d 0 -m 23 -j