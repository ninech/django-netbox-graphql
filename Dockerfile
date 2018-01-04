FROM ninech/netbox

RUN pip install graphene-django==1.3 graphene==1.4 graphql-core==1.1 snapshottest pytest

COPY docker /tmp/

RUN cat /tmp/settings.py >> /opt/netbox/netbox/netbox/settings.py
RUN cat /tmp/urls.py >> /opt/netbox/netbox/netbox/urls.py

COPY netbox-graphql /opt/netbox/netbox/netbox-graphql

