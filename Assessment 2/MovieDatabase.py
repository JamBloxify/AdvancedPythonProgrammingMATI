import requests # API requests
from tkinter import * # GUI
import customtkinter # GUI but cooler (Scrollable frame, combo box, etc)
from PIL import Image, ImageTk # Image handling
import io # Also image handling
import random # Random
import webbrowser # Open web browser for trailers
from tkinter import messagebox # for pop up messages. i could replace my print statements with it but too lazy
# so many imports but whatever

window = Tk()

# Backend stuff. I hate it
# --- Movie Class ---
class MovieApp:
    def __init__(self, apiKey): # Initialize the class with API
        self.api = apiKey
        self.baseURL = "https://api.themoviedb.org/3"


        self.headers = { # Needed to authenticate API requests specifically for TMDB because of their setup and bearer tokens or smthn
            "Authorization": f"Bearer {self.api}",
            "accept": "application/json"
        }


        print("MovieApp initialized with key:", apiKey)


    def getMovies(self, category): # Get movies based on category
        try:
            url = f"{self.baseURL}/movie/{category}?language=en-US&page=1"
            data = requests.get(url, headers=self.headers).json() # idk why it's unassigned, but dont touch it
        except Exception as error:
            print("Error getting movies:", error)
            return []
        print("Movie fetched")
        return data.get("results", [])


    def formatMovie(self, movieInfo): # Format movie info into a dictionary
        return {
            "ID": movieInfo.get("id"),
            "Title": movieInfo.get("title"),
            "Poster": movieInfo.get("poster_path"),
            "Overview": movieInfo.get("overview"),
            "Rating": movieInfo.get("vote_average")
        }

    
    def getRandomMovie(self): # Get a random movie
        page = random.randint(1, 500)
        
        try:
            url = f"{self.baseURL}/discover/movie?page={page}&language=en-US&sort_by=popularity.desc"
            data = requests.get(url, headers=self.headers).json()
            results = data["results"]
        except Exception as error:
            print("Error getting random movie:", error)
            return None
            
        movie = random.choice(results)
        return self.formatMovie(movie)
        print("Movie Randomized") # leave this alone
    

# -- Initialize API --
# Very long API key, idk why
APIKEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0MDc3OGRmYTVlNzJmYzUwOGZhOTliM2I5NTQyMjkyYSIsIm5iZiI6MTc2NDA1NzM4OC4zODIwMDAyLCJzdWIiOiI2OTI1NjEyYzRhMWZjMzM3ZWEyNmI3NTkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.tmfRYT2o-8jXxNJA2giOir5GsTl9I_JsgGwdQDKEKsk"
app = MovieApp(APIKEY)


# --- Functions ---
# I copypasted the card format before realizing i could function it
def makeMovieCard(movie): # Movie card GUI to avoid repetition
    mov = movie

    card = customtkinter.CTkFrame(frame, fg_color="#1A0B36", corner_radius=8)
    card.pack(pady=10, padx=10, fill="x")

    poster_path = mov.get("Poster")

    if poster_path:
        urlImg = f"https://image.tmdb.org/t/p/w200{poster_path}"
        dataImg = requests.get(urlImg).content
        img = Image.open(io.BytesIO(dataImg))
        img = img.resize((100, 150))
        tkImg = ImageTk.PhotoImage(img)
    else:
        print("No poster for", mov.get("Title"))
        tkImg = None

    imgLabel = Label(card, image=tkImg, bg="#1A0B36")
    imgLabel.image = tkImg
    imgLabel.pack(padx=10, pady=10, side=LEFT)

    infoFrame = customtkinter.CTkFrame(card, fg_color="transparent")
    infoFrame.pack(pady=10, side=LEFT, fill="both", expand=True)

    titleLabel = customtkinter.CTkLabel(infoFrame, text=mov.get("Title"), text_color='white', font=('Arial', 16, 'bold'))
    titleLabel.pack(anchor="w")

    rateLabel = customtkinter.CTkLabel(infoFrame, text=f"Rating: {mov.get('Rating')}", text_color='#eef36a', font=('Arial', 14))
    rateLabel.pack(pady=5, anchor="w")

    overview = mov.get("Overview")
    if len(overview) > 200:
        overview = overview[:200] + "..."
    descLabel = customtkinter.CTkLabel(infoFrame, text=overview, text_color='white', font=('Arial', 12), wraplength=260, justify="left")
    descLabel.pack(anchor="w")

    trailerBtn = customtkinter.CTkButton(infoFrame, text='Watch Trailer', fg_color=("#4dccbd"), hover_color=("#6df8e8"), text_color='black', font=('Arial', 12, 'bold'), command=lambda movieId=mov.get("ID"): movieTrailer(movieId))
    trailerBtn.pack(pady=5, anchor="w")

    infoBtn = customtkinter.CTkButton(infoFrame, text='More Info', fg_color=("#4dccbd"), hover_color=("#6df8e8"), text_color='black', font=('Arial', 12, 'bold'), command=lambda movieId=mov.get("ID"): movieInfo(movieId))
    infoBtn.pack(pady=5, anchor="w")

def clearFrame(): # Clear main frame for new content
    for widget in frame.winfo_children():
        widget.destroy()
    print("Frame cleared")


def valueChange(category): # Handles the combo box values
    CATEGORY = { # Mapping for categories in combo box to avoid errors. It's annoying
        "Popular": "popular",
        "Top Rated": "top_rated",
        "Now Playing": "now_playing",
        "Upcoming": "upcoming"
    }

    if category == "Filter by...": # Ignores default value or it causes bugs
        return

    clearFrame()

    home() # Resets search bar

    apiCategory = CATEGORY.get(category)

    baseMovies = app.getMovies(apiCategory)
    if not baseMovies: # If no results (very unlikely but whatever)
        resultsLabel = customtkinter.CTkLabel(frame, text="No results found.", text_color="white", font=('Arial', 14))
        resultsLabel.pack(pady=20)
        return

    movies = []
    for mov in baseMovies:
        movies.append(app.formatMovie(mov))
    for movie in movies:
        makeMovieCard(movie)


def searchMovies(event=None): # Search bar functionality. Event none is for binding
    input = searchBar.get().strip() # Get user input

    if not input: # do nothing if entry empty
        return

    clearFrame()

    home() # Resets search bar

    try:
        url = f"{app.baseURL}/search/movie?query={input}&language=en-US&page=1"
        data = requests.get(url, headers=app.headers).json()
        results = data["results"]
    except Exception as error:
        print("Error searching movies:", error)
        return

    results = data.get("results", [])
    movies = []

    if not results:
        resultsLabel = customtkinter.CTkLabel(frame, text="No results found.", text_color="white", font=('Arial', 14))
        resultsLabel.pack(pady=20)
        return

    for mov in results:
        movies.append(app.formatMovie(mov))

    for movie in movies:
        makeMovieCard(movie)

def showRandomMovie(): # Displays a random movie
    clearFrame()
    randomMovie()
    mov = app.getRandomMovie()
    makeMovieCard(mov)

def movieTrailer(movieId): # Movie trailer
    try:
        url = f"{app.baseURL}/movie/{movieId}/videos?language=en-US"
        data = requests.get(url, headers=app.headers).json()
    except Exception as error:
        messagebox.showerror("Error", "Error fetching trailer.")
        return

    results = data.get("results", [])
    for vid in results:
        if vid.get("site") == "YouTube" and vid.get("type") == "Trailer":
            trailerURL = f"https://www.youtube.com/watch?v={vid.get('key')}"
            webbrowser.open(trailerURL)
            return
        
    messagebox.showwarning("No Trailer", "Trailer not available for this movie.")

def movieInfo(movieId): # Movie info
    url = f"https://www.themoviedb.org/movie/{movieId}"
    webbrowser.open(url)






# --- GUI Tkinter ---
# -- Navbar --
navbar = Frame(window, bg="#160D34", width=1000, height=75)
navbar.pack(side=TOP)

title = Label(navbar, text="JAMES' MOVIE DATABASE", fg='#eef36a', bg='#160D34', font=('Arial', 20, 'bold underline'))
title.place(relx=0.5, rely=0.5, anchor=CENTER)

# - Home -
def home():
    global searchBar
    clearFrame()
    frameLabel = customtkinter.CTkLabel(frame, text="Welcome to the Movie Database!\nSearch for any movie\nOr generate a random one!", text_color='#eef36a', font=('Arial', 14, 'bold'), justify="center")
    frameLabel.pack(pady=20)
    searchBar = customtkinter.CTkEntry(frame, width=300, placeholder_text="Search for a movie", fg_color=("#1A0B36"), border_color=("#3E2A72"), text_color='white', font=('Arial', 14))
    searchBar.pack(pady=10)
    searchBar.bind("<Return>", searchMovies)

    filterCombo = customtkinter.CTkComboBox(frame, width=200, values=["Filter by...", "Popular", "Top Rated", "Now Playing", "Upcoming"], fg_color=("#1A0B36"), button_color=("#3E2A72"), text_color='white', font=('Arial', 14), state='readonly', command=valueChange)
    filterCombo.set("Filter by...")
    filterCombo.pack(pady=10)

# - Random Movie -
def randomMovie():
    clearFrame()
    randLabel = customtkinter.CTkLabel(frame, text="Random Movie", text_color='#eef36a', font=('Arial', 20, 'bold'))
    randLabel.pack(pady=10)

    randomMovieBtn = customtkinter.CTkButton(frame, text='Click for a Random Movie', fg_color=("#4dccbd"), hover_color=("#6df8e8"), text_color='black', font=('Arial', 12, 'bold'), command=showRandomMovie)
    randomMovieBtn.pack(pady=10)

# -- Main Frame --
frame = customtkinter.CTkScrollableFrame(window, width=450, height=500, fg_color=("#0E0821"))
frame.place(relx=0.5, rely=0.6, anchor=CENTER)

home() # Initialize home view

# -- Buttons --
homeButton = customtkinter.CTkButton(window, text="HOME", fg_color=("#4dccbd"), hover_color=("#6df8e8"), text_color='black', font=('Arial', 12, 'bold'), command=home)
homeButton.place(relx=0.3, rely=0.17, anchor=CENTER)

ranButton = customtkinter.CTkButton(window, text="RANDOM", fg_color=("#4dccbd"), hover_color=("#6df8e8"), text_color='black', font=('Arial', 12, 'bold'), command=randomMovie)
ranButton.place(relx=0.7, rely=0.17, anchor=CENTER)




# --- Window Config ---
window['bg'] = "#070410"
window.title("Movie Database")
window.geometry('500x700')
window.resizable(0, 0)
window.mainloop()
