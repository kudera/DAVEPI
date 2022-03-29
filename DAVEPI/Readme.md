To run:
    execute dave_api.py to start local server. You can update the config username, password to whatever you like.

access_point:
    http://127.0.0.1:5000

endpoints:
- `/sites`
    - `GET`: return all records from sites index
    - `POST`: Add a record to sites index. Takes arguments for `root_domain`, `domain_authority`, and `spam_score`
    - `DELETE`: Remove a record from sites index. Takes argument `root_domain`

- more to come
