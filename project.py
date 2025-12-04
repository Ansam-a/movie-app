import streamlit as st
import requests 

# --- Page Configuration ---
st.set_page_config(page_title="Netflix Checker", page_icon="🍿")

# --- My TMDB API Key ---
API_KEY = 'ab17ef0fe9d890c12fd097edf141a085'

# --- Local Movie List (Simulating Netflix Database) ---
movies_list = [
    "Stranger Things", "The Witcher", "Squid Game", "The Queen's Gambit",
    "Black Mirror", "Bridgerton", "Money Heist", "Dark", 
    "The Crown", "Emily in Paris", "Wednesday", "Narcos", 
    "Breaking Bad", "Better Call Saul", "Friends", "The Office", 
    "Inception", "Interstellar", "Spider-Man", "Joker",
    "Red Notice", "Extraction", "The Irishman", "Bird Box",
    "Glass Onion", "Enola Holmes", "Lucifer", "Ozark"
]

# Function to check if the movie exists in our local list
def check_movie(name):
    for m in movies_list:
        if name.lower() in m.lower():
            return True
    return False

# Function to get recommendations from TMDB API
def get_recs_direct(name):
    try:
        # 1. Search for the movie online to get its ID
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={name}&language=en-US"
        response = requests.get(search_url)
        data = response.json()
        
        if not data.get('results'):
            return ["No results found on TMDB."]
        
        # Get the ID of the first result
        movie_id = data['results'][0]['id']
        
        # 2. Get recommendations using the movie ID
        recs_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}&language=en-US"
        recs_response = requests.get(recs_url)
        recs_data = recs_response.json()
        
        final_list = []
        # Loop to get the top 5 movies
        for r in recs_data.get('results', [])[:5]:
            title = r.get('title', 'Unknown')
            date = r.get('release_date', 'N/A')[:4]
            final_list.append(f"{title} ({date})")
            
        if not final_list:
            return ["No specific recommendations found."]
            
        return final_list

    except Exception as e:
        return [f"Connection Error: {e}"]

# --- Main App Interface ---
st.title("🍿 Netflix Movie Checker")

search_text = st.text_input("Enter movie name:", placeholder="e.g. Barbie")

if st.button("Check Availability"):
    if search_text:
        # Check if movie is available locally
        found = check_movie(search_text)
        
        if found:
            st.success(f"✅ Yes! '{search_text}' is available on Netflix.")
            st.balloons()
        else:
            st.error(f"❌ '{search_text}' is NOT currently available.")
            
            st.subheader("💡 Recommended Alternatives:")
            
            # Fetch recommendations from API
            with st.spinner('Fetching from TMDB...'):
                suggestions = get_recs_direct(search_text)
            
            for s in suggestions:
                st.write(f"• {s}")

    else:
        st.warning("Please type a name first.")

# --- Footer / Attribution ---
st.markdown("---")
st.markdown("This product uses the TMDB API but is not endorsed or certified by TMDB.")