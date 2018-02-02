FROM ninech/netbox

ENV NETBOX_GRAPHQL_PATH /opt/netbox-graphql
ENV NETBOX_PATH /opt/netbox/netbox

COPY . ${NETBOX_GRAPHQL_PATH}
RUN pip install -e ${NETBOX_GRAPHQL_PATH}

COPY docker /tmp/
RUN cat /tmp/settings.py >> ${NETBOX_PATH}/netbox/settings.py && \
    cat /tmp/urls.py >> ${NETBOX_PATH}/netbox/urls.py && \
    ln -s ${NETBOX_GRAPHQL_PATH}/netbox-graphql ${NETBOX_PATH}/netbox-graphql
