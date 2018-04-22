wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.0/elasticsearch-2.4.0.tar.gz
tar -xvzf elasticsearch-2.4.0.tar.gz
cp -r elasticsearch-2.4.0 /opt/elasticsearch2
rm -rf elasticsearch-2.4.0
mkdir /datalog/elasticsearch2
mkdir /var/log/elasticsearch2
chown -R elasticsearch:elasticsearch /datalog/elasticsearch2
chown -R elasticsearch:elasticsearch /opt/elasticsearch2/
chown -R elasticsearch:elasticsearch /var/log/elasticsearch2

cat > /opt/elasticsearch2/config/elasticsearch.yml <<END
# ---------------------------------- Cluster -----------------------------------
cluster.name: production
# ------------------------------------ Node ------------------------------------
node.name: ${HOSTNAME}_2
node.master: false
node.data: true
# ----------------------------------- Paths ------------------------------------
path.data: /datalog/elasticsearch2/
path.logs: /var/log/elasticsearch2
# ----------------------------------- Memory -----------------------------------
bootstrap.mlockall: true
# ---------------------------------- Network -----------------------------------
network.host: [_bond0_, _local_]
http.port: 9201
transport.tcp.port: 9301
# --------------------------------- Discovery ----------------------------------
discovery.zen.ping.unicast.hosts: ["172.18.10.103:9300","172.18.10.106:9300","172.18.10.108:9300"]
discovery.zen.minimum_master_nodes: 2
# ----------
indices.memory.index_buffer_size: 40%
indices.breaker.fielddata.limit: 40%
indices.breaker.request.limit: 30%
indices.breaker.total.limit: 50%
node.box_type: hot
cluster.routing.allocation.same_shard.host: true
END

cat > /etc/systemd/system/elasticsearch2.service <<END
[Service]
Environment=ES_HOME=/opt/elasticsearch2
Environment=CONF_DIR=/opt/elasticsearch2/config
Environment=LOG_DIR=/var/log/elasticsearch2
Environment=PID_DIR=/var/run/elasticsearch
EnvironmentFile=-/etc/sysconfig/elasticsearch

WorkingDirectory=/opt/elasticsearch2

User=elasticsearch
Group=elasticsearch

ExecStart=/opt/elasticsearch2/bin/elasticsearch \
                                                -Des.pidfile=${PID_DIR}/elasticsearch2.pid \
                                                -Des.default.path.home=${ES_HOME} \
                                                -Des.default.path.logs=${LOG_DIR} \
                                                -Des.default.path.data=${DATA_DIR} \
                                                -Des.default.path.conf=${CONF_DIR}

StandardOutput=journal
StandardError=inherit

# Specifies the maximum file descriptor number that can be opened by this process
LimitNOFILE=65536

# Specifies the maximum number of bytes of memory that may be locked into RAM
# Set to "infinity" if you use the 'bootstrap.memory_lock: true' option
# in elasticsearch.yml and 'MAX_LOCKED_MEMORY=unlimited' in /etc/sysconfig/elasticsearch
LimitMEMLOCK=infinity

# Disable timeout logic and wait until process is stopped
TimeoutStopSec=0

# SIGTERM signal is used to stop the Java process
KillSignal=SIGTERM

# Java process is never killed
SendSIGKILL=no

# When a JVM receives a SIGTERM signal it exits with code 143
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target

# Built for Distribution: RPM-2.4.0 (rpm)
END

systemctl daemon-reload

echo "EDIT network.host trong file /opt/elasticsearch2/config/elasticsearch.yml"
