FROM mongo:7.0.0

COPY ./CS4010.accidents.json /CS4010.accidents.json
COPY ./CS4010.traffic_data.json /CS4010.traffic_data.json
COPY ./CS4010.traffic_registration_points.json /CS4010.traffic_registration_points.json

CMD mongoimport --host mongo --db CS4010 --collection accidents --mode upsert --type json --file /CS4010.accidents.json --jsonArray; \
    mongoimport --host mongo --db CS4010 --collection traffic_data --mode upsert --type json --file /CS4010.traffic_data.json --jsonArray; \
    mongoimport --host mongo --db CS4010 --collection traffic_registration_points --mode upsert --type json --file /CS4010.traffic_registration_points.json --jsonArray