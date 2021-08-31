# GameserverAuthenticationAPI
 An API for game servers to authenticate player accounts (minecraft style)


## Running the API

I suggest you take this script as a base, and use your own database and data structs. This part explains how to start the API running. I also suggest that you use something like NGINX to reverse proxy so you can add complex caching layers and can scale vertically a bit better.

### 1. Installing Libraries
`pip3 install -r requirements.txt`

### 2. Start the Server
`python3 server.py`

That should start the server. Now on to using it in your game.



## Authenticating Players

The authentication flow is quite simple. When a game client wants to connect to a server, it should send a request the `/authorize` with the username/password/deviceID or whatever else you want to use to authenticate players. The client will get get a one time use token that it should somehow communicate to the server it wants to connect to. Once the server has this token, the server can make its own independent request to `/grant` with the token to make sure that the player is who they say they are. The server should recieve a 200 OK with the player's data (retreived from database or however you get it). At that point, and only that point, can the player be allowed to spawn into the game.

                     Client (1) --[user/pass]----\ 
                     |   ^                        |
                    (2)  |                        V
                     |   \---------[token]------ API
                  [token]                          ^
                     |                             |
                     V                             |
                     GameServer (2) --[token]-----/

I'm sorry, this diagram sucks... Hopefully you understand.