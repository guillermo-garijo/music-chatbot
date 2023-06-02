import requests


def get_event_information(artists):
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    api_key = "GxuS8MSyTlbBK5XHdtzzbTHuIEVskIlC"  # Replace with your Ticketmaster API key

    event_info = []

    for artist in artists:
        params = {
            "keyword": artist,
            "apikey": api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract relevant information from the response
            print(data)
            events = data["_embedded"]["events"]
            for event in events:
                event_info.append({
                    "artist": artist,
                    "event_name": event["name"],
                    "venue": event["_embedded"]["venues"][0]["name"],
                    "date": event["dates"]["start"]["localDate"]
                })

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving information for {artist}: {e}")

    return event_info


def get_event_information(cities):
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    api_key = "GxuS8MSyTlbBK5XHdtzzbTHuIEVskIlC"  # Replace with your Ticketmaster API key

    event_info = []

    for city in cities:
        params = {
            "keyword": city,
            "apikey": api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract relevant information from the response
            #print(data)
            events = data["_embedded"]["events"]
            for event in events:
                event_info.append({
                    "event_name": event["name"],
                    "venue": event["_embedded"]["venues"][0]["name"],
                    "date": event["dates"]["start"]["localDate"],
                    "location": event["_embedded"]["venues"][0]["city"]['name']
                })

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving information for {city}: {e}")

    return event_info




#data=get_event_information(['imagine dragons', 'rosalia'])
#data=get_event_information(['barcelona', 'france'])


print(data)