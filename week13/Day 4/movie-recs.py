movies = [
    {'title': 'The Matrix', 'year': 1999, 'rating': 8.7, 'genre': 'Sci-Fi'},
    {'title': 'Inception', 'year': 2010, 'rating': 8.8, 'genre': 'Thriller'},
    {'title': 'Pulp Fiction', 'year': 1994, 'rating': 8.9, 'genre': 'Crime'},
    {'title': 'The Godfather', 'year': 1972, 'rating': 9.2, 'genre': 'Crime'},
    {'title': 'Avatar', 'year': 2009, 'rating': 7.8, 'genre': 'Sci-Fi'},
    {'title': 'Titanic', 'year': 1997, 'rating': 7.8, 'genre': 'Romance'}
]

# Sort movies by rating and year (descending order)
by_rating = sorted(movies, key=lambda x: x['rating'], reverse=True)
by_year = sorted(movies, key=lambda x: x["year"], reverse=True)

print("Highest rated:", by_rating[0]['title'])
print("Newest movie:", by_year[0]['title'])

# Create a lambda to classify movies by era
# - Year >= 2000: 'Modern'
# - Year >= 1990: 'Recent'
# - Otherwise: 'Classic'

classify_era = lambda year: 'Modern' if year >= 2000 else ('Recent' if year >= 1990 else 'Classic')

rating_category = lambda rating: 'Masterpiece' if rating >= 9.0 else ('Excellent' if rating >= 8.0 else 'Good')

print("Movie Classifications:")
for movie in movies:
    era = classify_era(movie['year'])
    category = rating_category(movie['rating'])
    print(f"{movie['title']}: {era}, {category}")
    
