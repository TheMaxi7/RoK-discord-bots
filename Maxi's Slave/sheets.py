import gspread

      
sa = gspread.service_account()

class KvkStats():   
    def __init__(self) -> None:
        self.filename = "Spreadsheet name"
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet("Sheet name")
    def get_player_stats(self, gov_id: int):
        str_id = str(gov_id)
        found_cell = self.main_worksheet.find(str_id)
        if found_cell is None:
            return None
        values = self.main_worksheet.row_values(found_cell.row)
        return dict(zip(self.main_worksheet.row_values(1), values))

class TopX():
    def __init__(self) -> None:
        self.filename = "Spreadsheet name"
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet("Sheet name")
    def top_x(self, ranks: int):
        #Cant loop 500+ times each time bot is triggered
        #Get all values we need, then we loop. 
        t4_column = self.main_worksheet.col_values(7)
        t5_column = self.main_worksheet.col_values(8)
        deads_column = self.main_worksheet.col_values(9)
        T4_in_top_x = 0
        T5_in_top_x= 0
        Deads_in_top_x = 0
        for x in range(1,ranks+1):
            T4_in_top_x += int(t4_column[x])
            T5_in_top_x += int(t5_column[x])
            Deads_in_top_x += int(deads_column[x])
        top_x_stats = [T4_in_top_x,T5_in_top_x,Deads_in_top_x]
        return top_x_stats

class DiscordDB():
    def __init__(self) -> None:
        self.filename = "Spreadsheet name"
        self.spreadsheet = sa.open(self.filename)
        self.main_worksheet = self.spreadsheet.worksheet("Sheet name")
    def get_id_from_discord(self, author_id: int):
        author_id_str= str(author_id)
        cell = self.main_worksheet.find(author_id_str)
        if cell is None:
            return None
        gov_id_str = self.main_worksheet.cell(cell.row, 2).value
        gov_id_int = int(gov_id_str)
        return gov_id_int    
    def save_dc_id(self, author_id: int, gov_id: int ):
        auth_id_str = str(author_id)
        gov_id_str = str(gov_id)
        id_cell = self.main_worksheet.find(auth_id_str)
        if id_cell is not None:
            self.main_worksheet.update_cell(id_cell.row, 2, gov_id_str)
        else:
            new_values = [auth_id_str,gov_id_str]
            self.main_worksheet.append_row(new_values, table_range="A2:B2")
