import cv2
import pytesseract
import numpy as np

from PIL import Image
from ultralytics import YOLO
from util import TroopDetection

troop_detection = TroopDetection()

def extract_deads(image):
    """
    Extract dead troops from an image.

    Args:
        image: The input image.

    Returns:
        tuple: Total T4 deads, total T5 deads, description.
    """
    model = YOLO('yolov8n.pt')
    model = YOLO(r'/app/weights/best.pt')  # Change path to best.pt accordingly

    troop_tiers = [5, 6, 7, 8, 9]
    troop_types = [1, 2, 3, 4]
    amounts = [0]

    troop_tiers_detections = []
    troop_types_detections = []
    troop_amounts_detections = []
    boxes = []

    tiers = {5: 'T1', 6: 'T2', 7: 'T3', 8: 'T4', 9: 'T5'}
    types = {1: 'Archers', 2: 'Cavalry', 3: 'Infantry', 4: 'Siege'}

    results = model(image)[0]

    for result in results.boxes.data.tolist():
        im_array = results.plot()
        x1, y1, x2, y2, score, class_id = result

        if int(class_id) in troop_tiers:
            troop_tiers_detections.append([x1, y1, x2, y2, class_id])
        elif int(class_id) in troop_types:
            troop_types_detections.append([x1, y1, x2, y2, class_id])
        elif int(class_id) in amounts:
            troop_amounts_detections.append([x1, y1, x2, y2])
        else:
            boxes.append([x1, y1, x2, y2])

    if (len(boxes) != len(troop_tiers_detections) or
            len(boxes) != len(troop_types_detections) or
            len(boxes) != len(troop_amounts_detections)):
        return None, None, None

    hall_of_heroes_dic = {}

    for box in boxes:
        x1_amount, y1_amount, x2_amount, y2_amount, troop_type, troop_tier = troop_detection.get_amount(
            troop_tiers_detections, troop_types_detections, troop_amounts_detections, box)
        amount_crop = im_array[int(y1_amount):int(y2_amount), int(x1_amount):int(x2_amount)]
        amount_crop_gray = cv2.cvtColor(amount_crop, cv2.COLOR_BGR2GRAY)
        _, amount_crop_thresh = cv2.threshold(amount_crop_gray, 100, 255, cv2.THRESH_BINARY)
        amount_crop_thresh = np.array(amount_crop_thresh)
        dead_amount = troop_detection.read_amount(amount_crop_thresh)

        if dead_amount is not None:
            hall_of_heroes_dic.setdefault(troop_tier, []).append((troop_type, dead_amount))
        else:
            print(f"Error processing tier: {troop_tier}, type: {troop_type}, dead_amount: {dead_amount}")

    total_t4_deads, total_t5_deads = 0, 0
    description = ""
    for tier in sorted(hall_of_heroes_dic.keys(), reverse=True):
        tier_results = hall_of_heroes_dic[tier]

        for troop_type, dead_amount in tier_results:
            if troop_type is None or dead_amount is None:
                return None, None, None
            elif tier == 8.0:
                total_t4_deads += int(dead_amount)
            elif tier == 9.0:
                total_t5_deads += int(dead_amount)

            description += f"{tiers[tier]} {types[troop_type]}: {dead_amount}\n"

    return total_t4_deads, total_t5_deads, description
