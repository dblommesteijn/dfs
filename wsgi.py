
# add src/ to sys.path
import sys, os
Q = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(Q + "/src"))

# import flask application
from dfs.cmds.serve import Serve, application

if __name__ == "__main__":
    application.run()
