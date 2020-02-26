# CTFTime Api Endpoint
Adds an endpoint to the CTFd api to allow for uploading the scores to [CTFtime.org](https://ctftime.org/)

This endpoint is designed to match CTFtime's [scoreboard feed specifications](https://ctftime.org/json-scoreboard-feeds)

The endpoint can be reached at `/api/v1/ctftime`

## Beware of challenge dependencies
This plugin shows the challenge name and value for all challenges that are visible. This includes challenges that should be hidden until their dependencies are solved.
