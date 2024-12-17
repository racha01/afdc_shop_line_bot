from typing import Any
from dataclasses import dataclass
import json
from datetime import datetime

@dataclass
class GetDataGoogleModel:
    id: str
    date: str
    amount: int
    total_amount: int
    
    def __init__(self, 
                 id: str = None, 
                 date: str = None,
                 amount: int = None,
                 total_amount: int = None):
        self.id = id
        self.date = date
        self.amount = amount
        self.total_amount = total_amount
        
    @staticmethod
    def from_dict(data_column: tuple, index: int, date: Any) -> 'GetDataGoogleModel':
        id = data_column[0]
        if data_column[1] is not None:
            date = date[index]
            amount = data_column[1]
        # if data_column[2] is not None:
        #     date = date[index + 1]
        #     amount = data_column[2]
            
        total_amount = data_column[2]
        return GetDataGoogleModel(id, amount, total_amount)
    
    @staticmethod
    def to_dict(id: str, date: str, amount: int, total_amount: int) -> 'GetDataGoogleModel':
        id = id
        date = date
        amount = int(amount)
        total_amount = int(total_amount)
        return GetDataGoogleModel(id, date, amount, total_amount)
    
    @staticmethod
    def from_Json(data: tuple) -> 'GetDataGoogleModel':
        id = data[0]['id']
        product_name = data[0]['product_name']
        return GetDataGoogleModel(id, product_name)