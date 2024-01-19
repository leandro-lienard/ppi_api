
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
import prex_cotizacion 

MAIN_ACCOUNT = 197663
CI = "INMEDIATA"
A_48HS = "A-48HS"
ppi = {}
LETRAS = "LETRAS"
BONOS = "BONOS" 

def login_account():
    Config = configparser.ConfigParser()
    Config.read("config.config")
    private_key = Config.get("Keys", "private_key")
    public_key = Config.get("Keys", "public_key")
    
    global ppi
    ppi = PPI(sandbox=False)
    ppi.account.login_api(public_key, private_key)   

def get_cotizacion(letra, tipo_instrumento, liquidacion):
    # print("\nSearching Current MarketData")
    current_market_data = ppi.marketdata.current(letra, tipo_instrumento, liquidacion)
    # print(current_market_data)
    return current_market_data
    
def get_ledes_value_usd(ledes_disp, letra, liquidacion):
    total_value = ledes_disp * get_cotizacion(letra , LETRAS, liquidacion)['price']
    print("\nfor %s %s the value is U$D %i MEP" % (letra, liquidacion, total_value))

def get_ledes_value_pesos(ledes_disp, letra, liquidacion):
    total_value = ledes_disp * get_cotizacion(letra , LETRAS, liquidacion)['price']
    print("\nfor %s %s the value is $%s pesos | cotizacion $%s" % (letra, liquidacion, format_number(total_value), format_number(total_value/POZO_A_SIMULAR)))
    
def get_bonos_value_usd(cant_disp, bono, liquidacion):
    total_value = cant_disp * get_cotizacion(bono, BONOS, liquidacion)['price']
    print("\nfor %s %s the value is U$D %i MEP" % (bono, liquidacion, total_value))

def get_bonos_value_pesos(cant_disp, bono, liquidacion):
    total_value = cant_disp * get_cotizacion(bono, BONOS, liquidacion)['price']
    print("\nfor %s %s the value is $%s pesos | cotizacion $%s" % (bono, liquidacion, format_number(total_value), format_number(total_value/POZO_A_SIMULAR)))
    
def format_number(number):
    return "{:,}".format(round(number))


POZO_A_SIMULAR = 1000 #usd ccl

def main():
    login_account()
    print("\nBuscando cotizacion LEDES mas conveniente with %i usd ccl" % POZO_A_SIMULAR)
    conclusion_text = ""

    ccl = get_cotizacion('XE4C',LETRAS, CI)
    mep_ci = get_cotizacion( 'XE4D', LETRAS, CI)
    mep_48hs = get_cotizacion( 'XE4D', LETRAS, A_48HS)
    pesos_ci = get_cotizacion( 'X18E4', LETRAS, CI)
    print("\nccl ci: %s \nmep ci %s \nmep 48hs %s \npesos ci %s" % (ccl, mep_ci, mep_48hs, pesos_ci))
    conclusion_text +=  "\nccl ci: %s \nmep ci %s \nmep 48hs %s \npesos ci %s" % (ccl, mep_ci, mep_48hs, pesos_ci)

    LEDES_disp = round( POZO_A_SIMULAR / float(ccl['price']))
    
    print("\nLEDES DISPONIBLES ", LEDES_disp)
    get_ledes_value_usd(LEDES_disp, 'XE4D', CI)
    get_ledes_value_usd(LEDES_disp, 'XE4D', A_48HS)
    get_ledes_value_pesos(LEDES_disp, 'X18E4', CI)
    
    #************************* BONOS AL 30 *****************************************
    ccl = get_cotizacion('AL30C', BONOS, CI)
    mep_ci = get_cotizacion('AL30D', BONOS, CI)
    mep_48hs = get_cotizacion('AL30D', BONOS, A_48HS)
    pesos_ci = get_cotizacion('AL30', BONOS, CI)

    print("\nAL30")    
    print("\nccl ci: %s \nmep ci %s \nmep 48hs %s \npesos ci %s" % (ccl, mep_ci, mep_48hs, pesos_ci))
    
    BONOS_DISP = round( POZO_A_SIMULAR / float(ccl['price']))
    
    print("\nAL30 DISPONIBLES ", BONOS_DISP) #precio cada 100 units?
    get_bonos_value_usd(BONOS_DISP, 'AL30D', CI)
    get_bonos_value_usd(BONOS_DISP, 'AL30D', A_48HS)
    get_bonos_value_pesos(BONOS_DISP, 'AL30', CI)
    
    #************************* BONOS GD 30 *****************************************
    ccl = get_cotizacion('GD30C', BONOS, CI)
    mep_ci = get_cotizacion('GD30D', BONOS, CI)
    mep_48hs = get_cotizacion('GD30D', BONOS, A_48HS)
    pesos_ci = get_cotizacion('GD30', BONOS, CI)

    print("\nGD30")    
    print("\nccl ci: %s \nmep ci %s \nmep 48hs %s \npesos ci %s" % (ccl, mep_ci, mep_48hs, pesos_ci))
    
    BONOS_DISP = round( POZO_A_SIMULAR / float(ccl['price']))
    
    print("\nGD30 DISPONIBLES ", BONOS_DISP) #precio cada 100 units?
    get_bonos_value_usd(BONOS_DISP, 'GD30D', CI)
    get_bonos_value_usd(BONOS_DISP, 'GD30D', A_48HS)
    get_bonos_value_pesos(BONOS_DISP, 'GD30', CI)
    
    
    #************************* PREX COTIZACION *****************************************
    pesos_prex = prex_cotizacion.get_pesos_totales(POZO_A_SIMULAR)
    print("\nPREX pesos: ", format_number(pesos_prex)) #precio cada 100 units?
    return conclusion_text

if __name__ == "__main__":
    main()
    