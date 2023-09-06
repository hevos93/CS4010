# Import statements
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas
import datetime
from time import sleep


# Constants
URL="https://www.vegvesen.no/trafikkdata/api/"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S+02:00"
END_TIME = datetime.datetime(year=2023, month=8, day=30, hour=0, minute=0, second=0)
TRPIDS = ["29403V625517","71241V2460301", "64557V625518", "29852V2460300", "73840V2041694"]
QUERY = gql(
    """
    query getTrafficData($TRPID: String!, $fromTime: ZonedDateTime!, $toTime: ZonedDateTime!) {
        trafficData(trafficRegistrationPointId: $TRPID){
            trafficRegistrationPoint {
            id
        }
                volume {
                byHour(
                    from: $fromTime
                    to: $toTime
                ){
                edges {
                    node {
                        from
                        to
                        total {
                            coverage {
                                percentage
                            }
                            volumeNumbers {
                                volume
                            }
                        }
                    }
                }
            }
            }
        }
    }
"""
)

# Functions 
def plusFour(original_date: str):
    timedate_date = datetime.datetime.strptime(original_date, TIME_FORMAT)
    plusfive_date = timedate_date + datetime.timedelta(days=4)
    string_plusfive = plusfive_date.strftime(TIME_FORMAT)
    return string_plusfive




# Main script
transport = AIOHTTPTransport(url=URL)
client = Client(transport=transport, fetch_schema_from_transport=True)

counter = 0
for TRPID in TRPIDS:
    dataset = []
    datetime_fromTime = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
    query_fromTime = datetime_fromTime.strftime(TIME_FORMAT)
    datetime_toTime = datetime.datetime(year=2020, month=1, day=5, hour=0, minute=0, second=0)
    query_toTime = datetime_toTime.strftime(TIME_FORMAT)
    
    limit = False

    while limit == False:
        print(TRPID + ":\t" , counter)
        params = {
            "TRPID": TRPID,
            "fromTime": query_fromTime,
            "toTime": query_toTime
        }
        result = client.execute(QUERY, variable_values=params)
        for item in result["trafficData"]["volume"]["byHour"]["edges"]:
            try:
                fromTime = item["node"]["from"]
                toTime = item["node"]["to"]
                coverage = item["node"]["total"]["coverage"]["percentage"]
                volume = item["node"]["total"]["volumeNumbers"]["volume"]
            except TypeError as e:
                print("ERROR: " , e)
                continue
            data = [fromTime, toTime, coverage, volume]
            dataset.append(data)
        
        query_fromTime = plusFour(query_fromTime)
        query_toTime = plusFour(query_toTime)
        params = {
            "TRPID": TRPID,
            "fromTime": query_fromTime,
            "toTime": query_toTime
        }

        check_fromTime = datetime.datetime.strptime(query_fromTime, TIME_FORMAT)
        if check_fromTime > END_TIME:
            limit = True

        sleep(0.25) # This is here so the connection is not dropped at the server end.
        counter = counter + 1

    pandas.DataFrame(dataset).to_csv(TRPID+".csv", header = ["fromTime", "toTime", "coverage", "volume"], index=False)