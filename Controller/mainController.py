from sql import *
class mainController:

    def index(self):
        print('index in mainController  ')


        return render_template("dashboard/graph.html")