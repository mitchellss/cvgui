# Core

Provides interfaces (protocols) that define the major 
functionality of the system. 

Overall, the system needs to do four major things:
- Recieve data from user
- Display visualization to user based on recieved data
- Optionally provide feedback via external devices
- Log required data

These four functions translate to the core packages of:
- `recieving`
- `displaying`
- `providing_feedback`
- `logging` (not yet implemented)

Core packages provide no implementation details, only method
stubs.
