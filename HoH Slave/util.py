import pytesseract
import gspread
sa = gspread.service_account()

# Change these names to set up your bot
SPREADSHEET_NAME = "KvK Discord Bot Stats"
SHEET_NAME = "Hall of Heroes"

pytesseract.pytesseract.tesseract_cmd = r'Path to tesseract.exe'  # Change path to tesseract.exe accordingly

class TroopDetection:
    def __init__(self, tolerance=0.1):
        self.tolerance = tolerance


    def get_amount(self, troop_tiers_detections, troop_types_detections, troop_amounts_detections, box):
        """
        Get troop amount, type, and tier from detections.

        Args:
            troop_tiers_detections: Troop tier detections.
            troop_types_detections: Troop type detections.
            troop_amounts_detections: Troop amount detections.
            box: Bounding box coordinates.

        Returns:
            Tuple containing amount coordinates, type, and tier.
        """
        x1_box, y1_box, x2_box, y2_box = box
        x1_amount, y1_amount, x2_amount, y2_amount = None, None, None, None
        type_, tier = None, None

        for j in range(len(troop_amounts_detections)):
            x1, y1, x2, y2 = troop_amounts_detections[j]
            if (x1 > x1_box - self.tolerance * (x2_box - x1_box) and
                y1 > y1_box - self.tolerance * (y2_box - y1_box) and
                x2 < x2_box + self.tolerance * (x2_box - x1_box) and
                y2 < y2_box + self.tolerance * (y2_box - y1_box)):
                x1_amount, y1_amount, x2_amount, y2_amount = int(x1), int(y1), int(x2), int(y2)

        for i in range(len(troop_types_detections)):
            x1, y1, x2, y2, class_id = troop_types_detections[i]

            if (x1 > x1_box - self.tolerance * (x2_box - x1_box) and
                y1 > y1_box - self.tolerance * (y2_box - y1_box) and
                x2 < x2_box + self.tolerance * (x2_box - x1_box) and
                y2 < y2_box + self.tolerance * (y2_box - y1_box)):
                type_ = class_id

        for k in range(len(troop_tiers_detections)):
            x1, y1, x2, y2, class_id = troop_tiers_detections[k]

            if (x1 > x1_box - self.tolerance * (x2_box - x1_box) and
                y1 > y1_box - self.tolerance * (y2_box - y1_box) and
                x2 < x2_box + self.tolerance * (x2_box - x1_box) and
                y2 < y2_box + self.tolerance * (y2_box - y1_box)):
                tier = class_id

        return x1_amount, y1_amount, x2_amount, y2_amount, type_, tier

    def read_amount(self, amount_crop):
        """
        Read the troop amount from an image.

        Args:
            amount_crop: Cropped image containing the amount.

        Returns:
            Cleaned troop amount as a string.
        """
        extracted_amount = pytesseract.image_to_string(amount_crop, config=r'--oem 3 --psm 6 outputbase digits')
        
        cleaned_amount = ""
        for char in extracted_amount:
            if char.isdigit() or char == '.' or char == ',':
                cleaned_amount += char
        
        cleaned_amount = cleaned_amount.replace(',', '') 
        cleaned_amount = cleaned_amount.replace('.', '')  
        
        return cleaned_amount


class Spreadsheet():
    def __init__(self) -> None:
        self.filename = SPREADSHEET_NAME
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet(SHEET_NAME)
    
    def register_stats(self, t4_deads, t5_deads, player_id):
        """
        Register stats in the spreadsheet.

        Args:
            t4_deads (int): Total T4 dead troops.
            t5_deads (int): Total T5 dead troops.
            player_id (int): Player's ID.
        """
        t4_deads_str = str(t4_deads)
        t5_deads_str = str(t5_deads)
        player_id_str = str(player_id)
        id_cell = self.main_worksheet.find(player_id_str)
        if id_cell is not None:
            self.main_worksheet.update_cell(id_cell.row, 2, t4_deads_str)
            self.main_worksheet.update_cell(id_cell.row, 3, t5_deads_str)
        else:
            new_values = [player_id_str, t4_deads_str, t5_deads_str]
            self.main_worksheet.append_row(new_values, table_range="A2:C2")

    
