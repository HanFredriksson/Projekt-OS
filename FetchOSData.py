import pandas as pd
import hashlib as hl


class OsDataFetcher:

    def __init__(self, file_path, en_col = None):
        """ Loads data from path. Functions to make filtered dataframes and save as csv file
        file_path: str - Local path to file
        en_col: str - Encrypts column and drops original column. Defult is None
        """
        self._path = file_path
        self.data = pd.read_csv(file_path)
        
        if en_col:
            self.encrypt_col(en_col)


    def os_filtered_dataframe(self, col, filter):
        """Retruns filtered a dataframe\n
        col: Column to filter from\n
        filter: What you want to filter out from rows\n
        return: A filterd pandas dataframe\n
        """

        df = self.data[self.data[col] == filter]

        return  df
    
    def encrypt_col(self, col):
        """Encrypts column "Name" to SHA256 hash key
        """
        try:
            self.data[col] = self.data[col].astype(str)
        
        except KeyError:
            print(f"There is no column named {col}.")

        hashes = self.data[col].apply(lambda name: hl.sha256(name.encode() ).hexdigest())
        self.data.insert(1, "Hash values", hashes)
        self.data.drop(columns=col, inplace=True)

    
    def os_data_saver(self, name, data): 
        """Save file as CSV in the original files path\n
        name: str - Name the file\n
        data: pd.df - Wich pandas dataframe to save\n
        """
        filepath = self._path.parent / f"{name}.csv"  

        filepath.parent.mkdir(parents=True, exist_ok=True)  

        data.to_csv(filepath)  