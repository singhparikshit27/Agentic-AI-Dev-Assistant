import requests
import json

def fetch_and_filter_github_events():
    url = "https://api.github.com/events"
    
    try:
        response = requests.get(url, timeout=10) # Add a timeout for robustness
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        events = response.json()
        
        if not isinstance(events, list):
            print("Error: API response is not a list of events.")
            return

        print("First 5 GitHub event types:")
        for i, event in enumerate(events[:5]):
            event_type = event.get('type')
            if event_type:
                print(f"  {i+1}. Type: {event_type}")
            else:
                print(f"  {i+1}. Type: N/A (type field missing)")

    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after 10 seconds while fetching data from {url}")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the internet or the server at {url}")
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP request failed with status code {e.response.status_code} - {e.response.reason}")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from the API.")
    except requests.exceptions.RequestException as e:
        print(f"An unexpected request error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_and_filter_github_events()