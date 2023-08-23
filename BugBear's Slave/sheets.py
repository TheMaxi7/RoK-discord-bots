import gspread

sa = gspread.service_account()

class DiscordDB:
    """
    Class for managing Discord-to-governor ID mappings.
    """

    def __init__(self) -> None:
        """
        Initialize the DiscordDB class.
        """
        self.filename = "Google spreadsheet name"
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet("sheet name")

    def get_id_from_discord(self, author_id: int):
        """
        Get governor ID from Discord author ID.

        Args:
            author_id (int): Discord author ID.

        Returns:
            int or None: Governor ID if found, None if not found.
        """
        author_id_str = str(author_id)
        cell = self.main_worksheet.find(author_id_str)
        if cell is None:
            return None
        gov_id_str = self.main_worksheet.cell(cell.row, 2).value
        gov_id_int = int(gov_id_str)
        return gov_id_int

    def save_dc_id(self, author_id: int, gov_id: int):
        """
        Save Discord author ID and governor ID mapping.

        Args:
            author_id (int): Discord author ID.
            gov_id (int): Governor ID.
        """
        auth_id_str = str(author_id)
        gov_id_str = str(gov_id)
        id_cell = self.main_worksheet.find(auth_id_str)
        if id_cell is not None:
            self.main_worksheet.update_cell(id_cell.row, 2, gov_id_str)
        else:
            new_values = [auth_id_str, gov_id_str]
            self.main_worksheet.append_row(new_values, table_range="A2:B2")

class Requirements:
    """
    Class for managing power-based requirements.
    """

    def __init__(self) -> None:
        """
        Initialize the Requirements class.
        """
        self.filename = "Google spreadsheet name"
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet("sheet name")

    def find_requirements(self, power: int):
        """
        Find kill and death requirements based on power.

        Args:
            power (int): Governor's power.

        Returns:
            tuple: Kill requirement and death requirement.
        """
        values_list = self.main_worksheet.col_values(1)
        power_list = [int(power) for power in values_list]
        for index in range(len(power_list) - 1, -1, -1):
            if power_list[index] <= power:
                kill_req = self.main_worksheet.cell(index + 1, 2).value
                deads_req = self.main_worksheet.cell(index + 1, 3).value
                return kill_req, deads_req
        return 0, 0
