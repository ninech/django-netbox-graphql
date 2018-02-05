FROM ninech/netbox

COPY . /opt/netbox-graphql
RUN pip install -e /opt/netbox-graphql

COPY docker /tmp/
RUN cat /tmp/settings.py >> /opt/netbox/netbox/netbox/settings.py && \
    cat /tmp/urls.py >> /opt/netbox/netbox/netbox/urls.py && \
    ln -s /opt/netbox-graphql/netbox-graphql /opt/netbox/netbox/netbox-graphql
