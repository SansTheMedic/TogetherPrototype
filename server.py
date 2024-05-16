import cherrypy
import random

class Session():
    # Initialization. Generates its storage and a random session code
    def __init__(self):
        self.users = []
        self.sessionCode = 0
        self.state = ""

        # Generates a random 32-bit integer for the room code, excluding 0
        self.sessionCode = random.randint(1,2147483647)

        # TEMP: test state body
        self.state = "This is session: " + str(self.sessionCode)
    
    # Getter function for the session code
    def GetCode(self):
        return self.sessionCode
    
    # Getter function for the state
    def GetState(self):
        return self.state
    
    # Setter function for the state, returns 1 if no error
    def SetState(self, newState):
        self.state = newState
        return 1
    
    # Getter function for users
    def GetUsers(self):
        return self.users
    
    # Function to check if a user is in this session
    def IsUser(self, user):
        if user in self.users:
            return True
        return False
    
    # Adds a user to the session, returns 1 if no error
    def AddUser(self,user):
        self.users.append(user)
        return 1
    
    # Removes a user from the session, returns 1 if no error
    def RemoveUser(self, user):
        if self.IsUser(user):
            self.users.remove(user)
            return 1
        else:
            return "WARN: this user wasn't in this session"


class HelloWorld(object):

    def __init__(self):
        # Our dictionary of sessions. Each session will be keyed by its code and contain the session object
        self.Sessions = {}

    @cherrypy.expose
    def index(self):
        return "Hello World!"
    
    @cherrypy.expose
    def JoinSession(self, session_code=0):
        # our url parameters come as strings, so we need to turn them to ints
        session_code = int(session_code)
        # Check if the session we're trying to connect to exists. If not, we create a new one
        if session_code not in self.Sessions.keys():
            session_code = self.CreateSession()

        # We also want to add the user to the session, if they aren't already
        # First we try to get the user cookie, if they have it
        try:
            this_user = cherrypy.request.cookie["User_id"]
        # If they don't we'll make a cookie for the user id, which will be another 32-bit integer
        except:
            new_id = random.randint(1,2147483647)
            cookie = cherrypy.response.cookie
            cookie["User_id"] = new_id
            this_user = cookie["User_id"]
        # Now we're sure there is a cookie for this user, we check if that user_id is in the session yet
        if this_user not in self.Sessions[session_code].GetUsers():
            self.Sessions[session_code].AddUser(this_user)
        return self.Sessions[session_code].GetState()

    # If a user is trying to join a session that doesn't exist, we call this to create a new one
    def CreateSession(self):
        session_code = 0
        session_made = False
        # While we don't have a session with a valid code
        while session_made == False:
            # Create a new session
            gen_session = Session()
            # Get the session code
            gen_code = gen_session.GetCode()
            # If our code is not already in use by an active session, save this session
            if gen_code not in self.Sessions.keys():
                session_made = True
                self.Sessions[gen_code] = gen_session
                session_code = gen_code
        
        return session_code

cherrypy.quickstart(HelloWorld())