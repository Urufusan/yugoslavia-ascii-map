def add_boardpin_emoji(text_argument="./asciiartyugo.mapready.txt", coordinates : tuple = None, ip_address=None, emoji = '📌', is_file = True):
    # Read the contents of the text file
    if is_file:
        with open(text_argument, 'r') as file:
            ascii_map = file.read()
    else:
        ascii_map = text_argument
    # Extract the top left and bottom right coordinates from the input
    top_left = (46.87306474114144, 13.436346074471219)
    bottom_right = (40.87923351493732, 22.92528116205865)
    
    # Split the ASCII map into lines
    lines = ascii_map.split('\n')
    
    # Calculate the dimensions of the ASCII map
    width = len(lines[0])
    height = len(lines)
    
    # Check if the given coordinates are within the map boundaries
    def is_within_bounds(coord):
        lat, lon = coord
        return top_left[0] >= lat >= bottom_right[0] and top_left[1] <= lon <= bottom_right[1]
    
    # Convert real-world coordinates to ASCII map coordinates
    def convert_to_map_coords(coord):
        lat, lon = coord
        x = int((lon - top_left[1]) / (bottom_right[1] - top_left[1]) * width) # (width +13))
        y = int((top_left[0] - lat) / (top_left[0] - bottom_right[0]) * height) # (height -1))
        return x, y

    # Add boardpin emoji to the specified coordinates (if provided)
    def add_boardpin(coords):
        x, y = coords
        lines[y] = lines[y][:x] + emoji + lines[y][x+1:]
    
    # Add boardpin emoji based on given coordinates
    if coordinates is not None:
        if is_within_bounds(coordinates):
            map_coords = convert_to_map_coords(coordinates)
            add_boardpin(map_coords)
        else:
            return "Out of bounds"
    
    # Add boardpin emoji based on IP address (if provided)
    if ip_address is not None:
        try:
            import requests
            response = requests.get(f'http://ip-api.com/json/{ip_address}')
            data = response.json()
            ip_coords = (float(data['lat']), float(data['lon']))
            if is_within_bounds(ip_coords):
                map_coords = convert_to_map_coords(ip_coords)
                add_boardpin(map_coords)
            else:
                return f"Out of bounds, source country: {data['country']}"
        except requests.exceptions.RequestException:
            return "Unable to fetch IP coordinates"
    
    # Join the modified lines and return the updated ASCII map as a string
    return '\n'.join(lines)

if __name__ == "__main__":
    text_file_path = 'path/to/yu.ascii.txt'
    coordinates = 44.809136541261275, 20.45569482562331 # Example coordinates (importable directly from google maps using right click -> coordinates)
    #ip_address = 'ljubljana.si'  # Example IP address
    baseplate = add_boardpin_emoji(coordinates=coordinates)# ip_address=ip_address)#)
    print(baseplate)
    ## Flags of nations example!
    #pinnies = ["🇷🇸","🇭🇷", "🇸🇮", "🇲🇰", "🇲🇪", "🇧🇦"]
    #[(),(),(),(),(),()]
    #krdntt = [(44.7866, 20.4489), (45.8150, 15.9819), (46.0569, 14.5058), (41.9973, 21.4280), (42.4304, 19.2594), (43.8563, 18.4131)]
    #for kord in krdntt:
    #    baseplate = add_boardpin_emoji(text_argument=baseplate, is_file=False, coordinates=kord)
    #    pass
    #result = baseplate
    #print(result)