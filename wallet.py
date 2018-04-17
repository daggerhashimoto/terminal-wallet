#!/usr/bin/env python3
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time,logging,json,sys
from terminaltables import AsciiTable, DoubleTable, SingleTable
from colorclass import Color, Windows
from progress.bar import ChargingBar

#logging.basicConfig()
#logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

RPC = AuthServiceProxy("http://rpcuser:rpcpassword@localhost:18332")

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

class color:
    BOLD = '\033[1m'
    END = '\033[0m'

def getunspent():
    unspentList = []
    for i in range(0,2):
        unspentList.append(RPC.listunspent(0)[i])
    return unspentList

def fill_table(unspentList):
    amountList = []
    addressList = []
    for i in range(0,len(unspentList)):
        amountList.append(unspentList[i]['amount'])
        addressList.append(unspentList[i]['address'])

    defaultList = ['Address' , 'Amount']
    
    # default table values
    TABLE_DATA = [
        [defaultList[0], defaultList[1]],
    ]
    # append list elements to table data
    for i in range(0,len(unspentList)):
        TABLE_DATA.append([addressList[i], amountList[i]])
    # print the table
    title = Color('{autogreen}Wallet{/autogreen}')
    table_instance = SingleTable(TABLE_DATA, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)

def latest_tx():
    txList = []
    for i in range(0,10):
        txList.append(RPC.listtransactions()[i])
        if txList[i]["category"] == "send":
            print(Color('{autored}' + txList[i]["address"] + " " + "-------->" + " " + str(txList[i]["amount"]) + '{/autored}'))
        else:
            print(Color('{autogreen}' + txList[i]["address"]+" "+ "<--------"+ " " + str(txList[i]["amount"]) + '{/autogreen}'))


while True:
    RPC = AuthServiceProxy("http://rpcusername:rpcpassword@localhost:18332") # added this here again otherwise rpc connection is timed out
    unspentList = getunspent()
    fill_table(unspentList)
    print("")
    print(color.BOLD + "Latest Wallet Transactions" + color.END)
    print("--------------------------\n")
    latest_tx()
    print("")
    sys.stdout = Logger("logfile.txt")
    bar = ChargingBar('Refreshing Transactions', max=60)
    for i in range(60):
        time.sleep(1)
        bar.next()
    bar.finish()

