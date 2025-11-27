import requests # API requests
from tkinter import * # GUI
import customtkinter # GUI but cooler (Scrollable frame, combo box, etc)
from PIL import Image, ImageTk # Image handling
import io # Also image handling
import random # Random
import webbrowser # Open web browser for trailers
from tkinter import messagebox # Message boxes

window = Tk()

# --- Movie Class ---
class MovieApp:
    def __init__(self, api):
        self.api = api
        self.baseURL = "https://api.themoviedb.org/3"
        self.headers = {
            "Authorization": f"Bearer {self.api}",
            "accept": "application/json"
        }

    def getMovies(self, category):
        url = f"{self.baseURL}/movie/{category}?language=en-US&page=1"
        data = requests.get(url, headers=self.headers).json()
        return data["results"]

    def formatMovie(self, rawMovie):
        return {
            "id": rawMovie.get("id"),
            "Title": rawMovie.get("title"),
            "Poster": rawMovie.get("poster_path"),
            "Overview": rawMovie.get("overview"),
            "Rating": rawMovie.get("vote_average")
        }

    
    def getRandomMovie(self):
        page = random.randint(1, 500)
        url = f"{self.baseURL}/discover/movie?page={page}&language=en-US&sort_by=popularity.desc"
        
        data = requests.get(url, headers=self.headers).json()
        results = data["results"]

        movie = random.choice(results)
        return self.formatMovie(movie)

# -- Initialize API --
APIKEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0MDc3OGRmYTVlNzJmYzUwOGZhOTliM2I5NTQyMjkyYSIsIm5iZiI6MTc2NDA1NzM4OC4zODIwMDAyLCJzdWIiOiI2OTI1NjEyYzRhMWZjMzM3ZWEyNmI3NTkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.tmfRYT2o-8jXxNJA2giOir5GsTl9I_JsgGwdQDKEKsk"
app = MovieApp(APIKEY)



# --- Functions ---
def makeMovieCard(movie): # Movie card GUI to avoid repetition
    card = customtkinter.CTkFrame(frame, fg_color="#1A0B36", corner_radius=8)
    card.pack(pady=10, padx=10, fill="x")

    poster_path = movie["Poster"]
    if poster_path:
        imgUrl = f"https://image.tmdb.org/t/p/w200{poster_path}"
        imgData = requests.get(imgUrl).content
        img = Image.open(io.BytesIO(imgData))
        img = img.resize((100, 150))
        tkImg = ImageTk.PhotoImage(img)
    else:
        tkImg = None

    imgLabel = Label(card, image=tkImg, bg="#1A0B36")
    imgLabel.image = tkImg
    imgLabel.pack(padx=10, pady=10, side=LEFT)

    infoFrame = customtkinter.CTkFrame(card, fg_color="transparent")
    infoFrame.pack(pady=10, side=LEFT, fill="both", expand=True)

    titleLabel = customtkinter.CTkLabel(infoFrame, text=movie["Title"], text_color='white', font=('Arial', 16, 'bold'))
    titleLabel.pack(anchor="w")

    rateLabel = customtkinter.CTkLabel(infoFrame, text=f"Rating: {movie['Rating']}", text_color='#eef36a', font=('Arial', 14))
    rateLabel.pack(pady=5, anchor="w")

    overview = movie["Overview"][:200] + "..."
    descLabel = customtkinter.CTkLabel(infoFrame, text=overview, text_color='white', font=('Arial', 12), wraplength=260, justify="left")
    descLabel.pack(anchor="w")

    trailerBtn = customtkinter.CTkButton(infoFrame, text='Watch Trailer', fg_color=("#4dccbd"), hover_color=("#6df8e8"), text_color='black', font=('Arial', 12, 'bold'), command=lambda m_id=movie.get("id"): openTrailer(m_id))
    trailerBtn.pack(pady=5, anchor="w")

    infoBtn = customtkinter.CTkButton(infoFrame, text='More Info', fg_color=("#4dccbd"), hover_color=("#6df8e8"), text_color='black', font=('Arial', 12, 'bold'), command=lambda m_id=movie.get("id"): openMoreInfo(m_id))
    infoBtn.pack(pady=5, anchor="w")

def clearFrame(): # Clear main frame for new content
    for widget in frame.winfo_children():
        widget.destroy()

CATEGORY = { # Mapping for categories in combo box to avoid errors
    "Popular": "popular",
    "Top Rated": "top_rated",
    "Now Playing": "now_playing",
    "Upcoming": "upcoming"
}

def valueChange(category): # Handles the combo box values
    if category == "Filter by...": # Ignores default value
        return

    clearFrame()

    home() # Resets search bar

    apiCategory = CATEGORY[category]

    rawMovies = app.getMovies(apiCategory)
    movies = [app.formatMovie(m) for m in rawMovies]

    for movie in movies:
        makeMovieCard(movie)


def searchMovies(event=None): # Search bar functionality
    input = searchBar.get().strip() # Get user input
    if not input:
        return

    clearFrame()

    home() # Resets search bar

    url = f"{app.baseURL}/search/movie?query={input}&language=en-US&page=1"
    data = requests.get(url, headers=app.headers).json()

    results = data.get("results", [])
    movies = [app.formatMovie(m) for m in results]

    if not movies: # If no results found
        noResult = customtkinter.CTkLabel(frame, text="No results found.", text_color="white", font=('Arial', 14))
        noResult.pack(pady=20)
        return

    for movie in movies:
        makeMovieCard(movie)

def showRandomMovie(): # Displays a random movie
    clearFrame()
    randomMovie()
    movie = app.getRandomMovie()
    makeMovieCard(movie)

def openTrailer(movie_id):
    if not movie_id:
        messagebox.showinfo("No Trailer", "Movie ID missing.")
        return

    url = f"{app.baseURL}/movie/{movie_id}/videos?language=en-US"
    data = requests.get(url, headers=app.headers).json()

    results = data.get("results", [])
    for v in results:
        if v.get("site") == "YouTube" and v.get("type") == "Trailer":
            trailerURL = f"https://www.youtube.com/watch?v={v.get('key')}"
            webbrowser.open(trailerURL)
            return

    messagebox.showinfo("No Trailer", "No trailer available for this movie.")

def openMoreInfo(movie_id):
    url = f"https://www.themoviedb.org/movie/{movie_id}"
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
