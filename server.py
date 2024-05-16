import cherrypy
import ottype
import random
import os, os.path
import threading

class Session():
    # Initialization. Generates its storage and a random session code
    def __init__(self):
        self.users = []
        self.sessionCode = 0
        self.state = ""

        # Generates a random 32-bit integer for the room code, excluding 0
        self.sessionCode = random.randint(1,2147483647)
    
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


class Liveshare(object):

    def __init__(self):
        # Our dictionary of sessions. Each session will be keyed by its code and contain the session object
        self.Sessions = {}
        # Our queue of Operation Transform Changes
        self.changes = []
        # A lock to ensure changes are handled one at a time
        self.lock = threading.Lock()

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
        
        # Lastly we need to create the redirect to the session page
        f = open("Session.html", "r")
        session_page = f.read()
        f.close()

        # Add the session code
        session_page = session_page.replace("[[SESSIONCODE]]", str(session_code))
        # Add the current state
        session_page = session_page.replace("[[CURRENTSTATE]]", self.Sessions[session_code].GetState())

        return session_page
    
    # AJAX based call to handle any time the user makes an edit
    @cherrypy.expose(["update"])
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def Update(self):
        # Get our json input
        input_json = cherrypy.request.json

        # Extract our data
        session_code = input_json["sessionCode"]
        adds = input_json["adds"]
        dels = input_json["dels"]

        # We want to turn our literal add and delete counters into Operations that OT understands
        operative_command = self.TurnToOperative(adds, dels)

        # Get the user from cookies
        this_user = cherrypy.request.cookie["User_id"]

        # Make sure that the user making this call is in the session
        if self.Sessions[session_code].IsUser(this_user) == True:
            # Add the operation to the queue
            self.changes.append(operative_command)

            # Lock our state temporarily to ensure only one command is used at once
            with self.lock:
                # Get the current state
                current_state = self.Sessions[session_code].GetState()

                # Get the next update. In theory, this should be the one that started this function
                operation = self.changes[0]
                # Remove that update from the queue
                self.changes.pop(0)

                # Apply that update to the state
                new_state = ottype.apply(current_state, operation)

                # Transform all remaining operations in the queue to bridge the change
                for i in range(len(self.changes)):
                    self.changes[i] = ottype.transform(self.changes[i], operation)
                
                # Apply the new state to the session
                self.Sessions[session_code].SetState(new_state)

            # Return our state to the user
            return {"error": False,
                    "msg": None,
                    "newState": self.Sessions[session_code].GetState()}
        else:
            return {"error": True,
                    "msg": "You aren't part of that session",
                    "newState": None}
        
    # AJAX based call to handle a user requesting an edit
    @cherrypy.expose(["fetch"])
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def DeliverUpdate(self, sessionCode):
        # turn out sessionCode back into an int
        session_code = int(sessionCode)

        # Get the user from cookies
        this_user = cherrypy.request.cookie["User_id"]

        # Make sure that the user making this call is in the session
        if self.Sessions[session_code].IsUser(this_user) == True:
            # Get the current state of the session
            current_state = self.Sessions[session_code].GetState()

            # Return our state to the user
            return {"error": False,
                    "msg": None,
                    "newState": current_state}
        else:
            return {"error": True,
                    "msg": "You aren't part of that session",
                    "newState": None}


    # If a user input_json[sessionCode]is trying to join a session that doesn't exist, we call this to create a new one
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
    
    # Turns a series of literals into Operative Transform terminology
    def TurnToOperative(self, adds, dels):
        # First we want to create a full list of literals
        literals = []
        for each_add in adds:
            literals.append([each_add[0], each_add[1], "a"])
        for each_del in dels:
            literals.append([each_del[0], each_del[1], "d"])

        # Then we want to sort our literals from the indexes they go to
        literals.sort(key= lambda x: x[1])

        # And now, we convert them into an OT term
        indextracker = 0
        OT = []
        for each_literal in literals:
            literal_index = each_literal[1]
            # If the index of this change is past our current index, we add a skip
            if literal_index > indextracker:
                skip = literal_index - indextracker
                OT.append(skip)
                indextracker = literal_index
            # Then, if the literal is an addition, plot it in
            if each_literal[2] == "a":
                OT.append(each_literal[0])
                # push the index tracker spaces equal to length of literal
                indextracker += len(each_literal[0])
            # Else it's a delete, so plot that in
            else:
                delete_token = {'d': each_literal[0]}
                OT.append(delete_token)
        
        # Finally we normalize the operation for use by the actual system
        OT = ottype.normalize(OT)
        return OT

    # Use Operative Transforms to make our changes
    def MakeChanges(self):
        pass

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(Liveshare(), '/', conf)