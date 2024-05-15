import gspread

#Change these names to setup your bot
SPREADSHEET_NAME = "KvK Discord Bot Stats"
STATS_SHEET = "Rankings"
TOPX_SHEET = "Rankings"
DISCORDID_SHEET = "DiscordID"


sa = gspread.service_account()

class KvkStats:
    """
    Class to fetch KvK stats from a Google Sheets spreadsheet.
    """
    def __init__(self) -> None:
        self.filename = SPREADSHEET_NAME
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet(f"{STATS_SHEET}")
    
    def get_player_stats(self, gov_id: int):
        """
        Get KvK stats for a player with the given governor ID.

        Args:
            gov_id (int): Governor ID.

        Returns:
            dict: Dictionary containing the player's stats.
        """
        str_id = str(gov_id)
        found_cell = self.main_worksheet.find(str_id)
        
        if found_cell is None:
            return None
        values = self.main_worksheet.row_values(found_cell.row)
        
        return dict(zip(self.main_worksheet.row_values(1), values))

class TopX:
    """
    Class to calculate cumulative top X stats from a Google Sheets spreadsheet.
    """
    def __init__(self) -> None:
        self.filename = SPREADSHEET_NAME
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet(f"{TOPX_SHEET}")
    
    def top_x(self, ranks: int):
        """
        Calculate cumulative top X stats.

        Args:
            ranks (int): Number of ranks to consider.

        Returns:
            list: List of cumulative top X stats [T4_in_top_x, T5_in_top_x, Deads_in_top_x].
        """
        t4_column = self.main_worksheet.col_values(7)
        t5_column = self.main_worksheet.col_values(8)
        deads_column = self.main_worksheet.col_values(9)
        T4_in_top_x = 0
        T5_in_top_x = 0
        Deads_in_top_x = 0
        for x in range(1, ranks + 1):
            T4_in_top_x += int(t4_column[x])
            T5_in_top_x += int(t5_column[x])
            Deads_in_top_x += int(deads_column[x])
        top_x_stats = [T4_in_top_x, T5_in_top_x, Deads_in_top_x]
        return top_x_stats

class Leaderboard:
    """
    Class to retrieve top 15 stats from a Google Sheets spreadsheet.
    """
    def __init__(self) -> None:
        self.filename = SPREADSHEET_NAME
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet(f"{STATS_SHEET}")

    
    def top_15(self):
        """
        Retrieve top 15 stats.

        Returns:
            list: List of top 15 player stats, where each player's stats are represented as a dictionary.
        """
        player_data = {}
        for row in range(2,17):
            player_stats = self.main_worksheet.row_values(row)
            player_rank = player_stats[1]
            player_name = player_stats[0]
            player_t4 = player_stats[6]
            player_t5 = player_stats[7]
            player_deads = player_stats[8]
            
            player_data[row-2]= [player_rank, player_name, player_t4, player_t5, player_deads]   
        return player_data


class DiscordDB:
    """
    Class to manage Discord IDs and corresponding governor IDs in a Google Sheets spreadsheet.
    """
    def __init__(self) -> None:
        self.filename = SPREADSHEET_NAME
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet(f"{DISCORDID_SHEET}")
    
    def get_id_from_discord(self, author_id: int):
        """
        Get governor ID associated with a Discord ID.

        Args:
            author_id (int): Discord user ID.

        Returns:
            int: Corresponding governor ID.
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
        Save Discord ID and governor ID association in the spreadsheet.

        Args:
            author_id (int): Discord user ID.
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