# # Prepare the image data
#     if image is not None:
#         # Convert PIL Image to bytes
#         buffered = io.BytesIO()
#         image.save(buffered, format="JPEG")
#         image_bytes = buffered.getvalue()
        
#         # Generate content
#         response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': image_bytes}])
#         return response.text

# C:\Users\Abhishek\OneDrive\Desktop\Medical_Chatbot