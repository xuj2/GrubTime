from tkinter import *
from tkinter import messagebox
import requests
import json
import random

API_KEY = ''
geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
detail_url = 'https://maps.googleapis.com/maps/api/place/details/json?'
restaurant_list = []

def firstPage():
    root = Tk()

    def geo_search():
        street_f = street.get().replace(' ', '+')
        city_f = city.get().replace(' ', '+')
        state_f = state.get()
        if len(street_f) == 0:
            messagebox.showerror("Error", "No street given!")
            return 0

        food_category = fc_val.get()
        distance = dist_val.get()

        full_url = geo_url + "address=" + street_f + ',+' + city_f + ',+' + state_f + API_KEY
        response = requests.get(full_url)
        data = response.json()
        r = data["results"][0]["geometry"]["bounds"]["northeast"]
        lat = r["lat"]
        lng = r["lng"]

        nearby_search(lat, lng, distance, food_category)
        
    def nearby_search(lat, lng, distance, food_category):
        coordinates = 'location=' + str(lat) + ',' + str(lng)
        radius = "&radius=" + str(int(distance) * 1609)
        search_type = "&type=restaurant"
        keyword = "&keyword=" + (food_category.replace(' ', '+'))

        full_url = search_url + coordinates + radius + search_type + keyword + API_KEY
        response = requests.get(full_url)
        data = response.json()
        r = data["results"]

        restaurant_list.clear()
        for restaurant in r:
            restaurant_list.append(restaurant)
        if len(restaurant_list) == 0:
            messagebox.showinfo("Message", 
            "No restaurant found within the distance of the given address! Make sure address is valid!")
            return 0

        root.destroy()
        secondPage()

    root.title('Grub Time')
    root.geometry('400x180')

    Label(root, text="Street:").place(x=50, y=10)
    street = Entry(root, width=19)
    street.insert(0, "17130 SE Rhododendron St")
    street.place(x=100, y=10)
    Label(root, text="City:").place(x=50, y=40)
    city = Entry(root, width=10)
    city.insert(0, "Happy Valley")
    city.place(x=80, y=40)
    Label(root, text="State:").place(x=180, y=40)
    state = Entry(root, width=6)
    state.insert(0, "OR")
    state.place(x=220, y=40)

    Label(root, text="Food category: ").place(x=50, y=70)
    fc_list = ["American", "Chinese", "Japanese", "Korean", "Mexican",
                 "Thai", "Vietnamese", "Fast Food", "Ramen", "Hotpot",
                 "Taco", "BBQ", "Sushi"]
    fc_val = StringVar()
    fc = OptionMenu(root, fc_val, *fc_list)
    fc.place(x=150, y=70)
    fc_val.set(fc_list[0])

    Label(root, text="Distance(miles): ").place(x=50, y=100)
    dist_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    dist_val = IntVar()
    dist = OptionMenu(root, dist_val, *dist_list)
    dist.place(x=160, y=100)
    dist_val.set(dist_list[0])

    button = Button(root, text="Find Restaurant", command=geo_search)
    button.place(x=140, y=130)

    root = mainloop()

def secondPage():
    root = Tk()

    def back():
        root.destroy()
        firstPage()

    def clear_result():
        name.delete(0, 'end')
        street.delete(0, 'end')
        phone.delete(0, 'end')
        rating.delete(0, 'end')
        hours.delete('1.0', 'end')
        show_result()

    def show_result():
        restaurant = random.choice(restaurant_list)
        place_id = restaurant["place_id"]
        full_url = detail_url + "place_id=" + place_id + API_KEY
        response = requests.get(full_url)
        data = response.json()
        r = data["result"]

        name.insert(0, r["name"])
        street.insert(0, r["vicinity"])
        phone.insert(0, r["formatted_phone_number"])
        r_n = r["user_ratings_total"]
        rate = r["rating"]
        rating_f = str(rate) + '/5.0' + '--with a total of ' + str(r_n) + ' reviews'
        rating.insert(0, rating_f)
        hours_f = ""
        if "opening_hours" in r:
            hour_list = r["opening_hours"]["weekday_text"]
            for h in hour_list:
                hours_f += h
                hours_f += "\n"
        else:
            hours_f = "No hours available to show"
        hours.insert('end', hours_f)

    root.title('Grub Time')
    root.geometry('460x320')

    back_button = Button(root, text="Back", command=back)
    back_button.place(x=0,y=0)
    pick_button = Button(root, text='Randomly pick again!', command=clear_result)
    pick_button.place(x=290,y=290)

    Label(root, text="Name: ").place(x=20, y=50)
    name = Entry(root,width=45,font=('Arial', 14))
    name.place(x=70,y=50)

    Label(root, text="Street: ").place(x=20, y=75)
    street = Entry(root,width=45,font=('Arial', 14))
    street.place(x=70,y=75)

    Label(root, text="Phone: ").place(x=20, y=100)
    phone = Entry(root,width=45,font=('Arial', 14))
    phone.place(x=70,y=100)

    Label(root, text="Hours: ").place(x=20, y=150)
    hours = Text(root,width=45,height=7,padx=4,pady=4,font=('Arial', 14))
    hours.place(x=70,y=150)

    Label(root, text="Rating: ").place(x=20, y=125)
    rating = Entry(root,width=45,font=('Arial', 14))
    rating.place(x=70,y=125)

    show_result()
    root = mainloop()

firstPage()
