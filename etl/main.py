from load import load_data

def main():
    while True:
        try:
            season = int(input("Enter the season you want to get data from: "))
            if season < 2000 or season > 2024:
                print("Please enter a valid season (e.g., 2024).")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number for the season.")
    load_data(season)

if __name__ == "__main__":
    main()