
import json

# Specify the path to your JSON file
json_file_path = "json_files/movies.json"

# Open the JSON file in read mode
with open(json_file_path, "r") as file:
    # Parse the JSON data into a Python list
    data = json.load(file)

    # Access the "title" for each object in the list
    titles_list = []
    for item in data:
        title = item.get("title")
        titles_list.append(title)

    # Print the list of titles
    print(titles_list)


# Specify the path to the output JSON file
output_file_path = "json_files/movies_list.json"

# Write the titles_list to the JSON file
with open(output_file_path, "w") as file:
    json.dump(titles_list, file, indent=2)
