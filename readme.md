# This is the indoor quantum localization tool.
For now, it just uses a Euclidean distance in an empty room.


# Install
To run the server, install pip python packages and run the flask server in `server.py` file.

We expect flask server will listen `http://localhost:5000`.

To see the visualization, just open the `index.html`. If the flask server is not up, classical algorithm's output will be in the console.
If the server is up, we will output our algorithm's output in the page itself. Check the backend's log for more details.