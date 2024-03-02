import json

def hello_world():
    message = "Hello, World! for the client!"
    data = {
        "message": message
    }
    json_data = json.dumps(data)
    return json_data

def main():
    print(hello_world())

if __name__ == "__main__":
    main()
