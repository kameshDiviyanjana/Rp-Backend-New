# from flask import Blueprint, request, jsonify
# import tensorflow as tf
# import base64
# from io import BytesIO
# from PIL import Image
# import numpy as np
# import os
# import traceback  # Import traceback for detailed error logging
# import json       # Import the json module

# writing_bp = Blueprint('writing', __name__)

# # Robust Model Loading
# model_path = os.path.join(os.path.dirname(__file__), "..", "model", "final_sinhala_letter_model.h5")
# try:
#     sinhala_letter_model = tf.keras.models.load_model(model_path)
#     print(f" ✔ Sinhala letter model loaded in writing_routes from: {model_path}")
# except Exception as e:
#     sinhala_letter_model = None
#     print(f"Error loading Sinhala letter model in writing_routes from {model_path}: {e}")

# sinhala_letters_json_str = """
# {
#   "1": "අ", "2": "ආ", "3": "ඇ", "4": "ඈ", "5": "ඉ", "6": "ඊ", "7": "උ", "8": "ඌ", "9": "ඍ", "10": "ඎ",
#   "11": "එ", "12": "ඒ", "13": "ඓ", "14": "ඔ", "15": "ඕ", "16": "ඖ", "17": "ක", "18": "ඛ", "19": "ග",
#   "20": "ඝ", "21": "ඞ", "22": "ච", "23": "ඡ", "24": "ජ", "25": "ඣ", "26": "ඤ", "27": "ට", "28": "ඨ",
#   "29": "ඩ", "30": "ඪ", "31": "ණ", "32": "ත", "33": "ථ", "34": "ද", "35": "ධ", "36": "න", "37": "ප",
#   "38": "ඵ", "39": "බ", "40": "භ", "41": "ම", "42": "ය", "43": "ර", "44": "ල", "45": "ව", "46": "ශ",
#   "47": "ෂ", "48": "ස", "49": "හ", "50": "ළ", "51": "ෆ", "52": "ක්‍රා", "53": "ක්‍රැ", "54": "ක්‍රෑ",
#   "55": "l%da", "56": ".%da", "57": "ඛ", "58": "ඛා", "59": "ඛි", "60": "ඛී", "61": "ඛ්", "62": "ඝ",
#   "63": "ඝා", "64": "ඝැ", "65": "ඝෑ", "66": "ඝි", "67": "ඝී", "68": "ඝු", "69": "ඝූ", "70": ">da",
#   "71": "ඝ්", "72": "ඝ්‍ර", "73": "ඝ්‍රා", "74": "ඝ්‍රි", "75": "ඝ්‍රී", "76": "ඳ", "77": "ඳා", "78": "ඳැ",
#   "79": "ෑ", "80": "ඳෑ", "81": "ඳි", "82": "ඳී", "83": "ඳු", "84": "ඳූ", "85": "|da ", "86": " ඳ්",
#   "87": "ඟ", "88": "ඟා", "89": "ඟැ", "90": " ඟෑ", "91": " ඟි", "92": "ඟී", "93": " ඟු", "94": " ඟූ",
#   "95": "Õda", "96": "ඟ්", "97": "ඬ", "98": "ැ", "99": "ඬා", "100": " ඬැ", "101": "ඬෑ", "102": " ඬි",
#   "103": "ඬී", "104": " ඬු", "105": "ඬූ", "106": "ඬda ", "107": " ඬ්", "108": "ඹ", "109": "ඹා", "110": " ඹැ",
#   "111": " ඹෑ", "112": " ඹි", "113": "ඹී", "114": " ඹු", "115": "ඹූ", "116": "Uda", "117": "ඹ්", "118": "භ",
#   "119": "භා", "120": "භැ", "121": "භෑ", "122": "භි", "123": "භී", "124": "භු", "125": "භූ", "126": "Nda",
#   "127": "භ්", "128": "ධ", "129": "ධා", "130": "ධැ", "131": "ධෑ", "132": ",ධි", "133": ",ධී", "134": ",ධු",
#   "135": ",ධූ", "136": "ධෝ", "137": "ධ්", "138": "ඨ", "139": "ඨා", "140": "ඨැ", "141": "ඨි", "142": "ඨී",
#   "143": "ඨු", "144": "ඨූ", "145": "ඨ්", "146": "ඪ", "147": "ඪා", "148": "ඪි", "149": "Vda", "150": "ඵ",
#   "151": "ඵා", "152": "ඵු", "153": "ඵි", "154": "Mda", "155": "ඵ් ", "156": "ථ", "157": "ථා", "158": "ථැ",
#   "159": "ථ්", "160": "ා", "161": "ෟ", "162": "ණැ", "163": "ණෑ", "164": "ෘ", "165": "ණී", "166": "ණු",
#   "167": "ණූ", "168": "Kda", "169": "ණ්", "170": "ඥ", "171": "ඥා", "172": "{da", "173": "ඤ", "174": "ඤා",
#   "175": "ඤු", "176": "[da", "177": "ඤ්", "178": "ඣ", "179": "ඣා", "180": "ඣු", "181": "COda", "182": "ඣ්",
#   "183": "ඦ", "184": "ඦා", "185": "ඦැ", "186": "ඦෑ", "187": "ඦි", "188": "ඦු", "189": "ඦූ", "190": "ඦෝ",
#   "191": "ඦ්", "192": "ඡ", "193": "ඡා", "194": "ඡැ", "195": "ඡෑ", "196": "ඡි", "197": "ඡේ", "198": "තැ",
#   "199": "තෑ", "200": "ත්‍රැ", "201": "ත්‍රෑ", "202": ";%da", "203": "ළු", "204": "ෲ", "205": "HQ", "206": "ff",
#   "207": "f", "208": "H", "209": "Hq"
#     }
#     """
# sinhala_letters_dict = json.loads(sinhala_letters_json_str) # Load JSON data into Python dictionary
# sinhala_letters = [sinhala_letters_dict[str(i+1)] for i in range(len(sinhala_letters_dict))] # Convert dict to LIST, ordered by keys (1, 2, 3, ...)


# @writing_bp.route('/process_letter', methods=['POST'])
# def process_letter_image():
#         if sinhala_letter_model is None:
#             return jsonify({"error": "Model not loaded"}), 500

#         data = request.get_json()
#         if not data or 'imageData' not in data:
#             return jsonify({"error": "No image data received"}), 400

#         image_data_url = data['imageData']
#         try:
#             # 1. Decode Base64 Data URL to image data
#             prefix, base64_str = image_data_url.split(',', 1)
#             image_bytes = base64.b64decode(base64_str)
#             image = Image.open(BytesIO(image_bytes)).convert('L') # Open as grayscale

#             # 2. Preprocessing: Resize and Normalize
#             image = image.resize((64, 64)) # Resize to 64x64
#             image_array = np.array(image) / 255.0 # Normalize to 0-1

#             # 3. Reshape for model input
#             image_array = np.expand_dims(image_array, axis=0) # Add batch dimension
#             image_array = np.expand_dims(image_array, axis=-1) # Add channel dimension

#             # 4. Model Prediction
#             prediction = sinhala_letter_model.predict(image_array)
#             predicted_class_index = np.argmax(prediction[0])

#             if 0 <= predicted_class_index < len(sinhala_letters):
#                 predicted_letter = sinhala_letters[predicted_class_index]
#                 confidence_score = float(prediction[0][predicted_class_index])
#             else:
#                 predicted_letter = "Unknown Letter"
#                 confidence_score = 0.0

#             # 5. Difficulty Adjustment Algorithm (Placeholder)
#             next_letter_suggestion = "ආ" #  Implement your difficulty algorithm here

#             # 6. Prepare and return response
#             response_data = {
#                 "predicted_letter": predicted_letter,
#                 "confidence_score": confidence_score,
#                 "next_letter_suggestion": next_letter_suggestion
#             }
#             return jsonify(response_data), 200

#         except Exception as e:
#             print(f"Error processing image: {e}")
#             return jsonify({"error": "Error processing image", "details": str(e)}), 500

from flask import Blueprint, request, jsonify
import tensorflow as tf
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import os
import traceback  # Import traceback for detailed error logging
import json       # Import the json module

writing_bp = Blueprint('writing', __name__)

# Robust Model Loading
model_path = os.path.join(os.path.dirname(__file__), "..", "model", "final_sinhala_letter_model.h5")
try:
    sinhala_letter_model = tf.keras.models.load_model(model_path)
    print(f" ✔ Sinhala letter model loaded in writing_routes from: {model_path}")
except Exception as e:
    sinhala_letter_model = None
    print(f"Error loading Sinhala letter model in writing_routes from {model_path}: {e}")


# ** IMPORTANT: REPLACE THIS LIST WITH YOUR ACTUAL SINHALA LETTER LIST IN THE CORRECT ORDER **
sinhala_letters_json_str = """
{
  "1": "අ", "2": "ආ", "3": "ඇ", "4": "ඈ", "5": "ඉ", "6": "ඊ", "7": "උ", "8": "ඌ", "9": "ඍ", "10": "ඎ",
  "11": "එ", "12": "ඒ", "13": "ඓ", "14": "ඔ", "15": "ඕ", "16": "ඖ", "17": "ක", "18": "ඛ", "19": "ග",
  "20": "ඝ", "21": "ඞ", "22": "ච", "23": "ඡ", "24": "ජ", "25": "ඣ", "26": "ඤ", "27": "ට", "28": "ඨ",
  "29": "ඩ", "30": "ඪ", "31": "ණ", "32": "ත", "33": "ථ", "34": "ද", "35": "ධ", "36": "න", "37": "ප",
  "38": "ඵ", "39": "බ", "40": "භ", "41": "ම", "42": "ය", "43": "ර", "44": "ල", "45": "ව", "46": "ශ",
  "47": "ෂ", "48": "ස", "49": "හ", "50": "ළ", "51": "ෆ", "52": "ක්‍රා", "53": "ක්‍රැ", "54": "ක්‍රෑ",
  "55": "l%da", "56": ".%da", "57": "ඛ", "58": "ඛා", "59": "ඛි", "60": "ඛී", "61": "ඛ්", "62": "ඝ",
  "63": "ඝා", "64": "ඝැ", "65": "ඝෑ", "66": "ඝි", "67": "ඝී", "68": "ඝු", "69": "ඝූ", "70": ">da",
  "71": "ඝ්", "72": "ඝ්‍ර", "73": "ඝ්‍රා", "74": "ඝ්‍රි", "75": "ඝ්‍රී", "76": "ඳ", "77": "ඳා", "78": "ඳැ",
  "79": "ෑ", "80": "ඳෑ", "81": "ඳි", "82": "ඳී", "83": "ඳු", "84": "ඳූ", "85": "|da ", "86": " ඳ්",
  "87": "ඟ", "88": "ඟා", "89": "ඟැ", "90": " ඟෑ", "91": " ඟි", "92": "ඟී", "93": " ඟු", "94": " ඟූ",
  "95": "Õda", "96": "ඟ්", "97": "ඬ", "98": "ැ", "99": "ඬා", "100": " ඬැ", "101": "ඬෑ", "102": " ඬි",
  "103": "ඬී", "104": " ඬු", "105": "ඬූ", "106": "ඬda ", "107": " ඬ්", "108": "ඹ", "109": "ඹා", "110": " ඹැ",
  "111": " ඹෑ", "112": " ඹි", "113": "ඹී", "114": " ඹු", "115": "ඹූ", "116": "Uda", "117": "ඹ්", "118": "භ",
  "119": "භා", "120": "භැ", "121": "භෑ", "122": "භි", "123": "භී", "124": "භු", "125": "භූ", "126": "Nda",
  "127": "භ්", "128": "ධ", "129": "ධා", "130": "ධැ", "131": "ධෑ", "132": ",ධි", "133": ",ධී", "134": ",ධු",
  "135": ",ධූ", "136": "ධෝ", "137": "ධ්", "138": "ඨ", "139": "ඨා", "140": "ඨැ", "141": "ඨි", "142": "ඨී",
  "143": "ඨු", "144": "ඨූ", "145": "ඨ්", "146": "ඪ", "147": "ඪා", "148": "ඪි", "149": "Vda", "150": "ඵ",
  "151": "ඵා", "152": "ඵු", "153": "ඵි", "154": "Mda", "155": "ඵ් ", "156": "ථ", "157": "ථා", "158": "ථැ",
  "159": "ථ්", "160": "ා", "161": "ෟ", "162": "ණැ", "163": "ණෑ", "164": "ෘ", "165": "ණී", "166": "ණු",
  "167": "ණූ", "168": "Kda", "169": "ණ්", "170": "ඥ", "171": "ඥා", "172": "{da", "173": "ඤ", "174": "ඤා",
  "175": "ඤු", "176": "[da", "177": "ඤ්", "178": "ඣ", "179": "ඣා", "180": "ඣු", "181": "COda", "182": "ඣ්",
  "183": "ඦ", "184": "ඦා", "185": "ඦැ", "186": "ඦෑ", "187": "ඦි", "188": "ඦු", "189": "ඦූ", "190": "ඦෝ",
  "191": "ඦ්", "192": "ඡ", "193": "ඡා", "194": "ඡැ", "195": "ඡෑ", "196": "ඡි", "197": "ඡේ", "198": "තැ",
  "199": "තෑ", "200": "ත්‍රැ", "201": "ත්‍රෑ", "202": ";%da", "203": "ළු", "204": "ෲ", "205": "HQ", "206": "ff",
  "207": "f", "208": "H", "209": "Hq"
    }
    """
sinhala_letters_dict = json.loads(sinhala_letters_json_str) # Load JSON data into Python dictionary
sinhala_letters = [sinhala_letters_dict[str(i+1)] for i in range(len(sinhala_letters_dict))] # Convert dict to LIST, ordered by keys (1, 2, 3, ...)


@writing_bp.route('/process_letter', methods=['POST'])
def process_letter_image():
        if sinhala_letter_model is None:
            return jsonify({"error": "Model not loaded"}), 500

        data = request.get_json()
        if not data or 'imageData' not in data:
            return jsonify({"error": "No image data received"}), 400

        image_data_url = data['imageData']
        try:
            # 1. Decode Base64 Data URL to image data
            prefix, base64_str = image_data_url.split(',', 1)
            image_bytes = base64.b64decode(base64_str)
            image = Image.open(BytesIO(image_bytes)).convert('L') # Open as grayscale

            # 2. Preprocessing: Resize and Normalize
            image = image.resize((64, 64)) # Resize to 64x64
            image_array = np.array(image) / 255.0 # Normalize to 0-1

            # **SAVE PREPROCESSED IMAGE - DEBUGGING**
            processed_image_path = "processed_image.png"  # Save in the flask directory
            pil_image = Image.fromarray((image_array * 255).astype(np.uint8).squeeze(), 'L') # Convert back to PIL Image and scale back for saving
            pil_image.save(processed_image_path)
            print(f"Saved preprocessed image to: {processed_image_path}")

            # 3. Reshape for model input
            image_array = np.expand_dims(image_array, axis=0) # Add batch dimension
            image_array = np.expand_dims(image_array, axis=-1) # Add channel dimension

            # **PRINT IMAGE ARRAY SHAPE - DEBUGGING**
            print(f"Preprocessed image array shape: {image_array.shape}") # Print the shape

            # 4. Model Prediction
            prediction = sinhala_letter_model.predict(image_array)
            predicted_class_index = np.argmax(prediction[0])

            if 0 <= predicted_class_index < len(sinhala_letters):
                predicted_letter = sinhala_letters[predicted_class_index]
                confidence_score = float(prediction[0][predicted_class_index])
            else:
                predicted_letter = "Unknown Letter"
                confidence_score = 0.0

            # 5. Difficulty Adjustment Algorithm (Placeholder)
            next_letter_suggestion = "ආ" #  Implement your difficulty algorithm here

            # 6. Prepare and return response
            response_data = {
                "predicted_letter": predicted_letter,
                "confidence_score": confidence_score,
                "next_letter_suggestion": next_letter_suggestion
            }
            return jsonify(response_data), 200

        except Exception as e:
            print(f"Error processing image: {e}")
            return jsonify({"error": "Error processing image", "details": str(e)}), 500