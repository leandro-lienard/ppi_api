##Documentacion https://itatppi.github.io/ppi-official-api-docs/api/documentacionPython/

from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.models.account_movements import AccountMovements
from ppi_client.models.bank_account_request import BankAccountRequest
from ppi_client.models.foreign_bank_account_request import ForeignBankAccountRequest, ForeignBankAccountRequestDTO
from ppi_client.models.cancel_bank_account_request import CancelBankAccountRequest
from ppi_client.models.order import Order
from ppi_client.models.order_budget import OrderBudget
from ppi_client.ppi import PPI
from ppi_client.models.order_confirm import OrderConfirm
from ppi_client.models.disclaimer import Disclaimer
from ppi_client.models.investing_profile import InvestingProfile
from ppi_client.models.investing_profile_answer import InvestingProfileAnswer
from ppi_client.models.instrument import Instrument
from datetime import datetime, timedelta
from ppi_client.models.estimate_bonds import EstimateBonds
import asyncio
import json
import traceback
import os
import configparser

MAIN_ACCOUNT = 197663
CI = "INMEDIATA"
A_48HS = "A-48HS"
ppi = {}

def login_account():
    Config = configparser.ConfigParser()
    Config.read("config.config")
    private_key = Config.get("Keys", "private_key")
    public_key = Config.get("Keys", "public_key")
    
    global ppi
    ppi = PPI(sandbox=False)
    ppi.account.login_api(public_key, private_key)   

def get_cotizacion_letra(letra, liquidacion):
    # print("\nSearching Current MarketData")
    current_market_data = ppi.marketdata.current(letra, "Letras", liquidacion)
    # print(current_market_data)
    return current_market_data
    
def get_ledes_value_usd(ledes_disp, letra, liquidacion):
    total_value = ledes_disp * get_cotizacion_letra(letra=letra, liquidacion=liquidacion)['price']
    print("\nfor %s %s the value is U$D %i MEP" % (letra, liquidacion, total_value))

def get_ledes_value_pesos(ledes_disp, letra, liquidacion):
    total_value = ledes_disp * get_cotizacion_letra(letra=letra, liquidacion=liquidacion)['price']
    print("\nfor %s %s the value is $ %s pesos" % (letra, liquidacion, format_number(total_value)))
    
def format_number(number):
    return "{:,}".format(round(number))


POZO_A_SIMULAR = 1000 #usd ccl

def main():
    login_account()
    print("\nBuscando cotizacion LEDES mas conveniente with %i usd ccl" % POZO_A_SIMULAR)
    
    ccl = get_cotizacion_letra(letra = 'XE4C', liquidacion=CI)
    mep_ci = get_cotizacion_letra(letra = 'XE4D', liquidacion=CI)
    mep_48hs = get_cotizacion_letra(letra = 'XE4D', liquidacion=A_48HS)
    pesos_ci = get_cotizacion_letra(letra = 'X18E4', liquidacion=CI)
    print("\nccl ci: %s \nmep ci %s \nmep 48hs %s \npesos ci %s" % (ccl, mep_ci, mep_48hs, pesos_ci))
    
    LEDES_disp = round( POZO_A_SIMULAR / float(ccl['price']))
    
    print("\nLEDES DISPONIBLES ", LEDES_disp)
    get_ledes_value_usd(ledes_disp=LEDES_disp, letra='XE4D', liquidacion=CI)
    get_ledes_value_usd(ledes_disp=LEDES_disp, letra='XE4D', liquidacion=A_48HS)
    get_ledes_value_pesos(ledes_disp=LEDES_disp, letra='X18E4', liquidacion=CI)
    
if __name__ == "__main__":
    main()
    