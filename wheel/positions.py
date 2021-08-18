import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.contract import * # @UnusedWildImport

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.contract = Contract()
        self.data = []  # Initialize variable to store candle
        self.df = pd.DataFrame()

    def nextValidId(self, orderId: int):
        # we can start now
        self.start()

    def start(self):
        self.accountOperations_req()
        print("Executing requests ... finished")

    def accountOperations_req(self):
        self.reqPositions()
        # self.aggregator()

    def position(self, account: str, contract: Contract, position: float,
                                   avgCost: float):
        super().position(account, contract, position, avgCost)
        # print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:", contract.secType,
        #       "Currency:", contract.currency,"Position:", position, "Avg cost:", avgCost)
        i = [account, contract.symbol, contract.secType, position, avgCost]
        #for i in self.data:
        self.data.append(i)
        print(self.data)
        if len(self.data) == 4:
            self.aggregator()

    def aggregator(self):
        self.df = pd.DataFrame(self.data, columns=['Account', 'Ticker', 'SecType', 'Position', 'Avg.Cost'])
        # if len(self.df) == 2:
        print(self.df)
        self.df.to_csv('positions.csv')
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()