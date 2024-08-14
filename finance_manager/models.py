class Transaction:
    def __init__(self, date, amount, category, description, transaction_type="expense"):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description
        self.transaction_type = transaction_type  # 'income' or 'expense'

    def __str__(self):
        return f"{self.date} | {self.amount} | {self.category} | {self.description} | {self.transaction_type}"
