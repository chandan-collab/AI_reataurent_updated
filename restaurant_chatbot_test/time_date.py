from datetime import datetime,date
# from config import url, key 
# # import supabase as sp
# from supabase import create_client, Client

# supabase: Client= create_client(url, key)

# # def db(code):
# #     menu = supabase.table('menu').select('*').execute()
# #     if menu.data:  # Check if data exists
# #         if code in menu.data:
# #             print(f"id : {code['item_code']}  name:{code['name']} \n")
# #     else:
# #         print("No data found in the 'menu' table.")
        
# # code=print("input the code : ")
# # print("name of food=",db(code))

# date1=date

# # time1=date.ctime()
# # time=time1.replace(microsecond=0,second=0)
# # print(time.isoformat())

# # print(date1.today())
# # print(date.day())
# # print(date.year())

# dt_string = "2025-04-14 10:30:00"
dt = datetime.now()
# print(f"Current date and time: {dt}")
# Split into date and time
# date_part = dt.date()
# time_part = dt.time().replace(microsecond=0)

# print("Date:", date_part)
# print("Time:", time_part)
# time_parts = dt.strftime("%M:%S").split(":")
# minutes, seconds = time_parts
# total_time = minutes + seconds
order_id = 5567
order_id += int(datetime.now().strftime("%M%S"))
print("Total (H+M+S):", order_id)

# print("new format",time)

# from supabase import create_client, Client
# from config import url, key 

# supabase = Client = create_client(url,key)
# def menu_keys(code):  
#     response = supabase.table('menu').select('*').execute()
#     primary_keys = {}

#     for item in response.data:  # Populate dictionary with item_code as key and name as value
#         primary_keys[item['item_code']] = item['name']
    
#     if code in primary_keys:  # Check if the code exists in the dictionary
#         return primary_keys[code]  # Print the name corresponding to the code 


# print("Menu name:", menu_keys(203)) # this will print the values of item code in the menu table

