import Levenshtein

# Search for similar matches using Levenshtein distance
search_term = 'example'
data = ['example', 'exmple', 'exampl', 'exmpale', 'exapmle']
results = []

# Iterate over the data to find matches
for item in data:
    distance = Levenshtein.distance(item, search_term)
    if distance <= 2:  # Adjust the threshold as needed
        results.append(item)

# Print the search results
if results:
    print("Search Results:")
    for result in results:
        print(result)
else:
    print("No matching results found.")


distance = Levenshtein.distance(string1, string2)
import Levenshtein
pip install python-Levenshtein
