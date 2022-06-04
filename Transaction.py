import mainWorker


class Transaction(object):
    blockNumber: int
    timeStamp: int
    timeStampReadable: str
    senderAddress: str
    amount: float
    confirmations: int
    chance: int

    def __init__(self):
        self.blockNumber = -1
        self.timeStamp = -1
        self.senderAddress = ''
        self.amount = -1
        self.confirmations = -1

    def __init__(self, input):
        self.blockNumber = int(input['blockNumber'])
        self.timeStamp = int(input['timeStamp'])
        self.senderAddress = input['from']
        self.amount = float(input['value']) / pow(10, 18)
        self.confirmations = int(input['confirmations'])
        self.timeStampReadable = mainWorker.timeStampToDate(self.timeStamp, '%d/%m %H:%M:%S')

    def printTransaction(self):
        print(f'Transaction from {self.senderAddress}, '
              f'at {mainWorker.timeStampToDate(self.timeStamp)}({self.timeStamp}) '
              f'amount of {self.amount} Ether. '
              f'Block no: #{self.blockNumber}, '
              f'{self.confirmations} confirmations.')