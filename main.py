from movie_importer import ReviewFetcher
from movie_logger import ReviewImporter
# Source account username
source_username = "enter_here_the_username_of_account_you_want_to_pull_from"

# Target account credentials
target_username = "your account"
target_password = "your password"

# Path to your ChromeDriver
chrome_driver_path = "chromedriver_path"

def main():
    # Fetch reviews from source account
    fetcher = ReviewFetcher(source_username)
    masterMovies = fetcher.get_all_movies()
    maxPageNum = fetcher.pageNum -1
    
    # Import reviews into target account
    importer = ReviewImporter(target_username, target_password, source_username,chrome_driver_path)
    importer.login_to_letterboxd()

    for pageNum in range(maxPageNum,0,-1):
        movies = masterMovies[pageNum]
        for movie in movies:
            importer.add_review_to_movies(movie["title"],movie["review"],pageNum)
    
    
    importer.close()

if __name__ == "__main__":
    main()