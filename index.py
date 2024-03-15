
from tkinter import *
import tkinter.messagebox
from random import *
#from tkinter import Label

class ScoreBoard:
    def __init__(self, parent):
        self.parent = parent
        self.initGUI()
        self.reset()

    def initGUI(self):
        # Lives
        self.livesVar = IntVar()
        Label(self.parent, text="Lives:", font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=35, pady=100, sticky=N+W)        
        Label(self.parent, textvariable=self.livesVar, font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=60, pady=150, sticky=N+W)        
       
        # Score
        self.scoreVar = IntVar()
        Label(self.parent, text="Score:", font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=35, pady=250, sticky=N+W)
        Label(self.parent, textvariable=self.scoreVar, font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=50, pady=300, sticky=N+W)        
       
        # High score
        self.highScoreVar = IntVar()
        Label(self.parent, text="Highest Score:", font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=0, pady=400, sticky=N+W)
        Label(self.parent, textvariable=self.highScoreVar, font=("Helvetica", 16, "bold")).grid(row=1, column=2, padx=50, pady=450, sticky=N+W)

    def reset(self):
        self.lives = 5
        self.score = 0
        self.highScore = self.loadScore()
       
        self.livesVar.set(self.lives)
        self.scoreVar.set(self.score)
        self.highScoreVar.set(self.highScore)

    def loadScore(self):
        with open("high-score.txt", "r") as data:
            return int(data.read())                
       
    def saveScore(self):
        if self.score > self.highScore:
            with open("high-score.txt", "w") as data:
                data.write(str(self.score))
       
    def gameOver(self):
        self.saveScore()
        tkinter.messagebox.showinfo("SYSTEM", "GAME OVER !")
        if self.score > self.highScore:
            self.highScoreVar.set(self.score)
            tkinter.messagebox.showinfo("High Score!", f"Congratulations! You've crossed the high score: {self.highScore}")
        if tkinter.messagebox.askyesno("SYSTEM", "Play Again ?"):
            self.reset()
        else:
            exit()

    def updateBoard(self, livesStatus, scoreStatus):
        self.lives += livesStatus
        self.score += scoreStatus
        if self.lives < 0:
            self.gameOver()
        self.livesVar.set(self.lives)
        self.scoreVar.set(self.score)


class ItemsFallingFromSky:
     def __init__(self, parent, canvas, player, board):
        self.parent = parent                    
        self.canvas = canvas                    
        self.player = player                    
        self.board = board                      
       
        self.fallSpeed = 50                          
        self.xPosition = randint(50, 750)      
        self.isgood = randint(0, 1)            
       
        self.goodItems = ["ananas.gif", "apple.gif", "orange.gif"]
        self.badItems = ["candy1.gif", "candy2.gif", "lollypop.gif"]
       
        if self.isgood:  
            self.itemPhoto = PhotoImage(file="images/{}".format(choice(self.goodItems)))
            self.fallItem = self.canvas.create_image((self.xPosition, 50), image=self.itemPhoto, tag="good")
        else:
            self.itemPhoto = PhotoImage(file="images/{}".format(choice(self.badItems)))
            self.fallItem = self.canvas.create_image((self.xPosition, 50), image=self.itemPhoto, tag="bad")
           
        self.move_object()

     def move_object(self):
        self.canvas.move(self.fallItem, 0, 15)
        if self.check_touching() or self.canvas.coords(self.fallItem)[1] > 650:
            self.canvas.delete(self.fallItem)
        else:
            self.parent.after(self.fallSpeed, self.move_object)

     def check_touching(self):
        x0, y0 = self.canvas.coords(self.fallItem)
        x1, y1 = x0 + 50, y0 + 50

        overlaps = self.canvas.find_overlapping(x0, y0, x1, y1)

        if self.canvas.gettags(self.fallItem)[0] == "good" and len(overlaps) > 1 and self.board.lives >= 0:
            self.board.updateBoard(0, 100)
            return True

        elif self.canvas.gettags(self.fallItem)[0] == "bad" and len(overlaps) > 1 and self.board.lives >= 0:
            self.board.updateBoard(-1, 0)
            return True

        return False


class Game:
    def __init__(self,parent):
        self.parent = parent
       
       
        self.parent.geometry("1024x650")
        self.parent.title("Catch My Food Game")

       
        self.canvas = Canvas(self.parent, width=800, height=600)
        self.canvas.config(background="skyblue")
        self.canvas.bind("<Key>", self.keyMoving)      
        self.canvas.focus_set()
        self.canvas.grid(row=1, column=1, padx=25, pady=25, sticky=W+N)

       
        self.playerPhoto = tkinter.PhotoImage(file = "images/{}" .format( "jew.gif" ) )
        self.playerChar = self.canvas.create_image( (475, 560) , image=self.playerPhoto , tag="player" )

       
        self.personalboard = ScoreBoard(self.parent)

        self.createEnemies()

    def keyMoving(self, event):
        if event.keysym == "Left":
            if self.canvas.coords(self.playerChar)[0] > 50:
                self.canvas.move(self.playerChar, -50, 0)
        elif event.keysym == "Right":
            if self.canvas.coords(self.playerChar)[0] < 750:
                self.canvas.move(self.playerChar, 50, 0)

    def createEnemies(self):
        ItemsFallingFromSky(self.parent, self.canvas, self.playerChar, self.personalboard)
        self.parent.after(1100, self.createEnemies)

class MainMenu:
   
    def __init__(self, parent):
        self.parent = parent
        self.parent.geometry("1024x650")
        self.parent.title("Catch Your Food Game")
        
        self.help_button = Button(self.parent, text="Help",font=("times",25,"bold"),bg="aquamarine",height=3,width=20, command=self.display_rules, fg="black")
        self.help_button.place(x=490,y=500, anchor=CENTER)

        self.start_button = Button(self.parent, text="Start Game",font=("times",25,"bold"),bg="greenyellow",height=3,width=20, command=self.start_game, fg="black")
        self.start_button.place(x=490, y=300, anchor=CENTER)
        label=Label(self.parent,text="CATCH YOUR FOOD",font=("times",70,"bold"),bg="pink")
        label.place(x=45,y=50)
        self.parent.configure(bg="#381150")
        
    def display_rules(self):
        rules = "Catch My Food Game Rules:\n\n" \
                "1. Move the character left and right using the left and right arrow keys.\n" \
                "2. Catch the good items to score points.\n" \
                "3. Avoid the bad items - they will reduce your lives.\n" \
                "4. You start with 5 lives. The game ends when lives reach 0.\n" \
                "5. Your highest score will be saved."

        tkinter.messagebox.showinfo("Game Rules", rules)

    def start_game(self):
        self.parent.destroy()
        game_window = Tk()
        game = Game(game_window)


if __name__ == "__main__":
    root = Tk()
    menu = MainMenu(root)
    root.mainloop()
