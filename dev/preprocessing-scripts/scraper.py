# Importing libraries
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas
import datetime
from time import sleep


# Constants
URL="https://www.vegvesen.no/trafikkdata/api/"
QUERY_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S+02:00"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
END_TIME = datetime.datetime(year=2023, month=8, day=30, hour=0, minute=0, second=0)
TRPIDS = ["29403V625517","71241V2460301", "64557V625518", "29852V2460300", "73840V2041694"]
QUERY = gql(
    """
    query getTrafficData($TRPID: String!, $fromTime: ZonedDateTime!, $toTime: ZonedDateTime!) {
     trafficData(trafficRegistrationPointId: $TRPID) {
    trafficRegistrationPoint {
      id
      location {
        coordinates {
          latLon {
            lon
            lat
          }
        }
        roadReference {
          shortForm
        }
      }
    }
    volume {
      byHour(from: $fromTime, to: $toTime) {
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

# Function to add four days to the input date, and return date in QUERY_TIME_FORMAT
def plusFour(original_date: str):
    timedate_date = datetime.datetime.strptime(original_date, QUERY_TIME_FORMAT)
    plusfive_date = timedate_date + datetime.timedelta(days=4)
    string_plusfive = plusfive_date.strftime(QUERY_TIME_FORMAT)
    return string_plusfive

# Main script
transport = AIOHTTPTransport(url=URL)
client = Client(transport=transport, fetch_schema_from_transport=True)

counter = 0

# For every TRP, get data
for TRPID in TRPIDS:
    dataset = []
    datetime_fromTime = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
    query_fromTime = datetime_fromTime.strftime(QUERY_TIME_FORMAT)
    datetime_toTime = datetime.datetime(year=2020, month=1, day=4, hour=0, minute=0, second=0)
    query_toTime = datetime_toTime.strftime(QUERY_TIME_FORMAT) 
    limit = False

    # Continue querying the API for data as long as we have not exceeded the end timestamp
    while limit == False:
        print(TRPID + ":\t" , counter)
        params = {
            "TRPID": TRPID,
            "fromTime": query_fromTime,
            "toTime": query_toTime
        }
        result = client.execute(QUERY, variable_values=params)

        try: 
            id = result["trafficData"]["trafficRegistrationPoint"]["id"]
            lon = result["trafficData"]["trafficRegistrationPoint"]["location"]["coordinates"]["latLon"]["lon"]
            lat = result["trafficData"]["trafficRegistrationPoint"]["location"]["coordinates"]["latLon"]["lat"]
            shortForm = result["trafficData"]["trafficRegistrationPoint"]["location"]["roadReference"]["shortForm"]
        except TypeError as e:
            print("ERROR: ", e)
            continue

        for item in result["trafficData"]["volume"]["byHour"]["edges"]:
            try:
                fromTime = item["node"]["from"].replace("T", " ").split("+")[0]
                toTime = item["node"]["to"].replace("T", " ").split("+")[0]
                coverage = item["node"]["total"]["coverage"]["percentage"]
                volume = item["node"]["total"]["volumeNumbers"]["volume"]
            except TypeError as e:
                print("ERROR: " , e)
                continue
            data = [id, shortForm, fromTime, toTime, coverage, volume, lon, lat]
            dataset.append(data)
        
        query_fromTime = plusFour(query_fromTime)
        query_toTime = plusFour(query_toTime)
        params = {
            "TRPID": TRPID,
            "fromTime": query_fromTime,
            "toTime": query_toTime
        }

        check_fromTime = datetime.datetime.strptime(query_fromTime, QUERY_TIME_FORMAT)
        if check_fromTime > END_TIME:
            limit = True

        sleep(1) # Included so the connection is not dropped at the server end.
        counter = counter + 1

    # Write the dataset dataframe to csv, writing a csv file for each TRP
    pandas.DataFrame(dataset).to_csv(TRPID+".csv", header = ["trpid", "roadReference", "fromTime", "toTime", "coverage", "volume", "lon", "lat"], index=False)