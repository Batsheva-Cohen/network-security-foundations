
### My JSON payload
{
  "user_name": "Batsheva Cohen",
  "age": 25,
  "is_active": true,
  "middle_name": null,
  "skills": ["Python", "Automation", "JSON, uv"],
  "address": {
    "city": "Jerusalem",
    "street": "bareket",
    "house_number": 2
  }
}


**The command**
echo '{
  "user_name": "Batsheva Cohen",
  "age": 25,
  "is_active": true,
  "middle_name": null,
  "skills": ["Python", "Automation", "JSON, uv"],
  "address": {
    "city": "Jerusalem",
    "street": "bareket",
    "house_number": 2
  }
}' | uv run python -m json.tool


{
    "user_name": "Batsheva Cohen",
    "age": 25,
    "is_active": true,
    "middle_name": null,
    "skills": [
        "Python",
        "Automation",
        "JSON, uv"
    ],
    "address": {
        "city": "Jerusalem",
        "street": "bareket",
        "house_number": 2
    }
}

**The command with error**
echo '{
  "user_name": "Batsheva Cohen",
  "age": 25,
  "is_active": true,
  "middle_name": null,
  "skills": ["Python", "Automation", "JSON, uv"],
  "address": {
    "city": "Jerusalem",
    "street": "bareket",
    "house_number": 2
}' | uv run python -m json.tool

**Error Message:** Expecting ',' delimiter: line 2 column 1 (char 221)From its perspective, the parser is currently looking at the address field, which contains a nested object. It doesn't inherently understand that a closing curly brace is missing to terminate the object; instead, it assumes a comma is required to append another key-value pair. Because the parser processes the input character by character and lacks a "big picture" view, it expects a comma to continue the object block. Consequently, it throws an error stating that a comma delimiter is missing.

**Extracting a nested value**
import json

my_payload = """{
  "user_name": "Batsheva Cohen",
  "age": 25,
  "is_active": true,
  "middle_name": null,
  "skills": ["Python", "Automation", "JSON", "uv"],
  "address": {
    "city": "Jerusalem",
    "street": ["A","B","C"],
    "house_number": 2
  }
}"""
data = json.loads(my_payload)
print(data['address']['street'][1:])

**Path Explanation**
data['address']: Retrieves the third element named "address", which contains 3 items within the dictionary.
['street']: Retrieves the item with the "street" key, which contains a list.
[1:]: Slices the list from the first index (the second item) until the end.

**JSON Schema**
 represents the predefined rules for how the data should be. It essentially determines the structure of the JSON, xactly what everything is supposed to contain and what the structure is, so that someone doesn't just change something out of nowhere since things are clear to everyone in advance
 the data types it must contain, the number of fields in each element, etc. It will contain the schema identifier and include all the rules. Schema validation is useful for testing because, beyond the status code I receive, I want to know that nothing broke during the test in the rest of the fields and everything remains valid. This prevents future bugs for me, allows me to know about them in advance, and ensures that the entire team knows e
**The Importance of Content-Type**
The Content-Type is the header sent under the -H flag that we use in API testing. It is mandatory to send the format of the content being transmitted under the -H flag when dealing with JSON. Otherwise, the server will parse it as plain text and will obviously not know that it needs to locate the keys and values within it. Consequently, the test will fail, and I will not receive a 200 OK status code.