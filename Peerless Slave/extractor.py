import cv2
import pytesseract
import numpy as np
import json
from PIL import Image
from fuzzywuzzy import fuzz

PATH_TO_JSON = 'questions.json'
#pytesseract.pytesseract.tesseract_cmd = r'Path to tesseract.exe'  # Change path to tesseract.exe accordingly

def are_strings_similar(string1, string2, threshold=85):
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

def find_extraction_region(image, debug=False):
    """
    Compare two strings and return True if they are similar for at least the specified threshold percentage.

    Args:
        string1 (str): The first string.
        string2 (str): The second string.
        threshold (int): The minimum similarity percentage required for a match.

    Returns:
        bool: True if the strings are similar for at least the threshold percentage, False otherwise.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    _, threshed_image = cv2.threshold(inverted_image, 170, 230, cv2.THRESH_BINARY)
    blurred_image = cv2.GaussianBlur(threshed_image, (5, 5), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    morphed_image = cv2.morphologyEx(blurred_image, cv2.MORPH_CLOSE, kernel)

    edges_image = cv2.Canny(morphed_image, 150, 600)

    if debug:
        cv2.imshow("edges", edges_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    regions, _ = cv2.findContours(edges_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_area = 0
    selected_region = None

    image_area = image.shape[0] * image.shape[1]

    for region in regions:
        _, _, region_width, region_height = cv2.boundingRect(region)
        area = region_width * region_height

        if area > largest_area and area > 0.1 * image_area:
            largest_area = area
            selected_region = region

    if selected_region is None:
        corners = np.array([
            [0, 0],
            [image.shape[1] - 1, 0],
            [image.shape[1] - 1, image.shape[0] - 1],
            [0, image.shape[0] - 1]
        ])
        selected_region = corners.reshape((-1, 1, 2))

    return selected_region

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
    
    return None, None

def extract_info_from_image(image, debug=False):
    """
    Extract information from an image.

    Args:
        image (numpy.ndarray): The input image.
        debug (bool): If True, display debug information.

    Returns:
        tuple: A tuple containing the extracted question and its corresponding answer.
    """
    ratio = image.shape[1] // image.shape[0]
    if 200 < image.shape[0] < 1200:
        resized_image = cv2.resize(image, (int(1200 * ratio), 1200))
        image = resized_image

    extraction_region = find_extraction_region(image)
    x, y, width, height = cv2.boundingRect(extraction_region)
    extraction_bounds = (x, y, width, height)

    if height > 200:
        height = height // 3
        y = y + 75
        width = width - 60

    question_crop = image[y:y+height, x:x+width]
    question_crop_gray = cv2.cvtColor(question_crop, cv2.COLOR_BGR2GRAY)
    _, question_crop_inverted = cv2.threshold(question_crop_gray, 120, 255, cv2.THRESH_BINARY)

    if debug:
        cv2.imshow('question_crop', question_crop)
        cv2.imshow('resized_image', image)
        cv2.imshow('Cropped Image', question_crop_inverted)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    extracted_text = pytesseract.image_to_string(question_crop_inverted, config=r'--oem 3 --psm 7 -l eng tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.\?"')

    question, answer = find_answer_to_question(extracted_text)

    return question, answer