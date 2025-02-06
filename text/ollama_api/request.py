import requests
from requests.auth import HTTPBasicAuth

def get_user_input():
    """prompt the user for input and return it"""
    return input("Enter your prompt(or type 'exit' to quit)")

def send_request(prompt):
    """Send a POST request to the Flask server with the given prompt."""
    url = "http://172.20.253.8:5000/run_command"
    payload = {"prompt":prompt}

    response = requests.post(url, json=payload, auth=HTTPBasicAuth('<your_username>', "<your_password>"))

    #check if the response was successful
    if response.status_code ==200:
        return response
    else:
        return {"error": f"Request failed with status code {response.status_code}"}
    
def main():
        """Main function to run the prompt loop"""
        while True:
            try:
                user_input = get_user_input()

                if user_input.lower() == "exit":
                    print("Exiting the program")
                    break
                response = send_request(user_input)

                # Check if the response is a valid response object
                if isinstance(response, requests.Response):
                    # Print the JSON content of the response
                    print(response.json())  # This will print the JSON response
                else:
                    print(response)  # Print error message if not a valid response


                print(response)
            except KeyboardInterrupt:
                print("\nExiting the program.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()








#Define the URL and the payload
url = "http://172.20.253.8:5000/run_command"

