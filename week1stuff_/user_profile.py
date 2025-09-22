def format_user_profile(user_data):
    # New feature: Calculate age
    from datetime import date
    age = date.today().year - user_data["birth_year"]

    print(f"Username: {user_data['username']}")
    print(f"Email: {user_data['email']}")
    print(f"Age: {age}") # Print the new calculated age

# Add birth_year to the dictionary
user_dict = {
    "username": "waleed",
    "email": "wale3dpr0@gmail.com",
    "birth_year": 2000 # Example birth year
}

format_user_profile(user_dict)