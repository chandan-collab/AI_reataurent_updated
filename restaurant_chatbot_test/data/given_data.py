import cv2

base_url = "https://8609-117-247-174-37.ngrok-free.app/static"
MENU_IMAGE_URLS = [
    f"{base_url}/menu_screenshot_compressed.jpg",
    f"{base_url}/instructions1.jpg"
#     f"{base_url}/menu3.jpg",
#     f"{base_url}/menu4.jpg",
#     f"{base_url}/menu5.jpg"
 ]
# ?t=raw forces the Supabase URL to serve the image directly with the proper content type.
#"https://drive.google.com/uc?id =  1QG9euVD2YNmrpjoFHRAJ9a1C6Ya26Kyx", use gd drive like this for access menu jpg/image
                





INSTUCTIONS="Act as a Restaurant assistant answer the questions related restaurant aslo describe benefits of asked food or item related food. if 'ok' , 'yes' , 'thankyou' or related to this kind of messages reply 'Thankyou for choosing us' otherwise ask them to type 'menu' for menu and 'need help' for help.If adult message or pornograpy related content told user to 'we ere going to block you soon'."

def compress_image(image_path, output_path, quality=35): #100 is best quality, and 0 is lowest quality
    img = cv2.imread(image_path)
    cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
#twilio has file size limits, and screenshots can be large.