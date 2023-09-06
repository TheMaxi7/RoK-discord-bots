import cv2
import pytesseract
import numpy as np
import json
from PIL import Image
from fuzzywuzzy import fuzz

PATH_TO_JSON = 'questions.json'
#pytesseract.pytesseract.tesseract_cmd = r'Path to tesseract.exe'  # Change path to tesseract.exe accordingly

def are_strings_similar(string1, string2, threshold=95):
    """
    Compare two strings and return True if they are similar for at least the specified threshold percentage.

    Args:
        string1 (str): The first string.
        string2 (str): The second string.
        threshold (int): The minimum similarity percentage required for a match.

    Returns:
        bool: True if the strings are similar for at least the threshold percentage, False otherwise.
    """
    similarity_ratio = fuzz.ratio(string1, string2)
    return similarity_ratio >= threshold


def find_answer_to_question(question):
    """
    Find an answer to a given question in a JSON file.

    Args:
        question (str): The question to find an answer for.

    Returns:
        tuple: A tuple containing the question and its corresponding answer.
    """
    with open(PATH_TO_JSON, 'r') as file:
        question_answer_pairs = json.load(file)

    for pair in question_answer_pairs:
        if are_strings_similar(pair['question'], question):
            return pair['question'], pair['answer']

    return "Missing", "Missing"


def extract_info_from_image(img, debug=False):
    """
    Extract information from an image.

    Args:
        img (numpy.ndarray): The input image.
        debug (bool): If True, display debug information.

    Returns:
        tuple: A tuple containing the extracted question and its corresponding answer.
    """
    target_color = (211, 41, 41)

    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    lower_bound = np.array([target_color[0] - 20, target_color[1] - 20, target_color[2] - 20])
    upper_bound = np.array([target_color[0] + 20, target_color[1] + 20, target_color[2] + 20])

    mask = cv2.inRange(img, lower_bound, upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if w >= 20 and h >= 20:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            blue_start_x = x + w
            blue_start_y = y
            blue_end_x = blue_start_x + (w * 19)
            blue_end_y = blue_start_y + (h * 3)

            cv2.rectangle(img, (blue_start_x, blue_start_y), (blue_end_x, blue_end_y), (255, 0, 0), 2)
            question_crop = img[int(blue_start_y):int(blue_end_y), int(blue_start_x):int(blue_end_x)]
            question_crop_gray = cv2.cvtColor(question_crop, cv2.COLOR_BGR2GRAY)
            _, question_crop_inverted = cv2.threshold(question_crop_gray, 120, 255, cv2.THRESH_BINARY)
            extracted_text = pytesseract.image_to_string(question_crop_inverted, config=r'--oem 3 --psm 6 -c tessedit_char_whitelist=" 1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.\?"')
            question, answer = find_answer_to_question(extracted_text)

            if debug:
                cv2.imshow("Original Image with Rectangles", img)
                cv2.imshow("question_crop", question_crop)
                cv2.imshow("question_crop_inverted", question_crop_inverted)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print(extracted_text)

            return question, answer

    return "Error", "Error"
      
  
