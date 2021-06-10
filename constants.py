
STATUS1_OPTIONS = (
    'Paid by Tpine', 'Tpine/ DP', 'Funded by CWB', 'Funded by DMF',
    'Warehouse BDC', 'Funded by BDC', 'Funded by BFC', 'Funded by Coast Capital',
    'Funded by RBC', 'Funded by VFS', 'Paid by PGL', 'Funded by Securcor', 'Funded by NL',
    'Funded by RCAP', 'BUY OUT', 'Cancelled', 'HAPPY NEW YEAR'
)

STATUS1_EXCLUSION_LIST = (
    'BUY OUT', 'Cancelled', 'Swapped', 'HAPPY NEW YEAR',
    'Insurance claim', 'SWAPPED', 'US Deal', 'Claim Received'
)

PROVINCES = (
    'AB', 'BC', 'MB', 'NB', 'NL', 'NU', 'NS', 'NT', 'ON', 'PE', 'QC', 'SK', 'YT'
)

# Application Colors
APP_BG_COLOR = '#f2f7f4'
#APP_BG_COLOR = '#c2a28c'
SEA_GREEN = '#6f9e59'
STRIPED_ROW_COLOR = '#dcebd5'

# Application Fonts
APP_DEFAULT_FONT = ('Segoe UI', 10)
APP_MENU_FONT = ('Segoe UI', 9)

LEASE_BASE_PATH = "P:/Tpine Leasing/"
FUNDER_TAO_PATH = "P:/Tpine Leasing/2021/TAO"
FUNDER_BFC_PATH = "P:/Tpine Leasing/2021/BFC"
FUNDER_COAST_PATH = "P:/Tpine Leasing/2021/Coast"
LOCAL_DB_PATH_HOME = r'D:\Contract Management.accdb;'
LAN_DB_PATH = r'P:\Tpine Leasing\2020\Amit/Contract Management.accdb;'
LOCAL_DB_PATH_OFF = r'C:\Amit\Contract Management.accdb;'
LIVE_DB_PATH = r'P:\Abdul\Contract Management.accdb'

# Constants for Data Fields
LEASE_NO = 0
SEQUENCE = 1
APPLICANT = 2
FIRST_NAME = 3
LAST_NAME = 4
ADDRESS = 5
CITY = 6
PROVINCE = 7
POSTAL = 8
HOME_PHONE = 9
BUSINESS_PHONE = 10
CELL_PHONE = 11
SALES_PERSON = 12
YEAR = 13
MAKE = 14
MODEL = 15
VIN = 16
VENDOR = 17
TERM = 18
REMAINING_TERM = 19
FREQUENCY = 20
APPROVED_ON = 21
FIRST_PAYMENT_DATE = 22
SELLING_PRICE = 23
DOWN_PAYMENT = 24
ADMIN_FEE_TPINE = 25
DOWN_RECEIVED = 26
FIN_AMOUNT = 27
RENTAL = 28
GAP = 29
PAYMENT_BEFORE_TAX = 30
TAX = 31
TOTAL_PAYMENT = 32
END_OF_TERM = 33
FICO = 34
BNI = 35
CREDIT_RATING = 36
STATUS_1 = 37
STATUS_2 = 38
TRANCHE = 39
FUNDED_ON = 40
BUYOUT_DATE = 41
BUYOUT_FUNDER = 42
AMOUNT_RECEIVED = 43
CURRENT_STATUS = 44
STATUS_DATE = 45
HOLDBACK = 46
HOLDBACK_REL_1 = 47
DATE = 48
HOLDBACK_REL_2 = 49
DATE_1 = 50
HOLDBACK_BALANCE = 51
PAP_DATE = 52
LEASE_ASSOCIATE = 53
PAYMENT_TYPE = 54
SCHEDULE = 55
DMF_RESERVE = 56
RESERVE_AMOUNT = 57
RESERVE_RELEASE = 58
RELEASE_DATE = 59
RESERVE_BALANCE = 60
