from datetime import datetime
from langchain_core.tools import tool

@tool
def check_date() -> str:
    """
    Trả về ngày tháng năm, thời gian hiện tại.
    """
    current_date = datetime.now()
    return current_date
