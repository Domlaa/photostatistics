from analysis.analyzer.data_analyzer import DataAnalyzer
from analysis.analyzer.mysql_data_analyzer import MysqlDataAnalyzer
from common.db_type import DBTYPE
from process.processor.data_processor import DataProcessor
from process.processor.mysql_data_processor import MysqlDataProcessor

db_type = DBTYPE.MYSQL

mysql_analyzer = MysqlDataAnalyzer()

def get_analyzer() -> DataAnalyzer:
    if db_type == DBTYPE.MYSQL:
        return mysql_analyzer
    if db_type == DBTYPE.SQLITE:
        raise ValueError(f"Unsupported DB type: {db_type}")
    else:
        raise ValueError(f"Unsupported DB type: {db_type}")



mysql_processor = MysqlDataProcessor()
def get_processor() -> DataProcessor:
    if db_type == DBTYPE.MYSQL:
        return mysql_processor
    if db_type == DBTYPE.SQLITE:
        raise ValueError(f"Unsupported DB type: {db_type}")
    else:
        raise ValueError(f"Unsupported DB type: {db_type}")