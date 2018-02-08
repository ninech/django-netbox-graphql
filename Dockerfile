FROM ninech/netbox

COPY . /opt/netbox-graphql
RUN pip install /opt/netbox-graphql[test]

COPY docker /tmp/
RUN cat /tmp/settings.py >> /opt/netbox/netbox/netbox/settings.py && \
    cat /tmp/urls.py >> /opt/netbox/netbox/netbox/urls.py && \
    ln -s /opt/netbox-graphql/netbox_graphql /opt/netbox/netbox/netbox_graphql
