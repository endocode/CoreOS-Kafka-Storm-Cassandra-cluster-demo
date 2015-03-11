#!/bin/bash

ZK_SED=""
for i in `echo "$ZK" | tr ',' "\\n"`; do
	if [ "x$i" != "x" ]; then
		if [ "x$ZK_SED" != "x" ]; then
			ZK_SED=`echo "$ZK_SED\\n  - \"$i\""`
		else
			ZK_SED=`echo "  - \"$i\""`
		fi
	fi
done

sed -i -e "s/%zk%/$ZK_SED/g" $STORM_HOME/conf/storm.yaml
sed -i -e "s/%nimbus%/$NIMBUS_HOST/g" $STORM_HOME/conf/storm.yaml
echo "storm.local.hostname: $HOST_NAME" >> $STORM_HOME/conf/storm.yaml

supervisord
