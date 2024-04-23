# Simple Chatroom system

A Simple Python chatroom system that uses both IP and Bluetooth protocols, if you find any problems or flaws don't hesitate to contact me!

The chatroom works by selecting the type of connection both on the server and client (Bluetooth or IP based).
The server acts as a chatroom Admin, so it can send and view messages like other members, in addition, it can also use a small set of special commands.

**Note:** *This isn't exactly one of my best codes and it has many flaws, this is my first time using Threading and socket  handling.*

## Libraries

libraries used in this project:
- socket *(built-in)*;
- threading *(built-in)*;
- colorama.

## Commands

Commands that the chatroom admin (server) can use:
- /help - Displays this message;
- /kick [nickname] - Kick a user from the chat;                
- /list - List of all connected users.

**Note:** *I will add a ban command in the future.*

## Known issues

As I said before this code is far from perfect, so here are some known issues that I found (hopefully I will fix them in the future):
- The communication isn't protected;
- Poor error handling;
- if someone sends a message while you are writing it will mess up your unsent input text (if you then send it the message will be displayed correctly) (I have no idea how to fix this)
