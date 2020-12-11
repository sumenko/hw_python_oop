# coding: utf-8
import datetime as dt
import random


class Calculator:
    """Общий класс для вычислений"""
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Сохраняет новую запись о расходах."""
        self.records.append(record)

    def get_date(self, delta_days=0):
        """Возвращает сегодняшнюю дату либо дату на delta дней назад."""
        today = dt.datetime.now().date()
        return today - dt.timedelta(days=delta_days)

    def get_today_stats(self):
        """Возвращает число, сколько денег/калорий потрачено сегодня."""
        today = self.get_date()
        today_amount = 0
        for record in self.records:
            if record.date == today:
                today_amount += record.amount
        return today_amount

    def get_today_left(self):
        """Возвращает сколько на сегодня осталось условных единиц."""
        return self.limit - self.get_today_stats()

    def show_all_records(self):
        """Выводит содержимое калькулятора, для отладки."""
        print("Содержимое калькулятора:")
        print("="*50)
        for record in self.records:
            print(f"{record.date.__str__():<10} {record.comment:<30}"
                  f"{record.amount:<8}")
        print("="*50)

    def get_week_stats(self):
        today = self.get_date()
        week_ago = self.get_date(7)
        amount = 0
        for record in self.records:
            if week_ago <= record.date <= today:
                amount += record.amount
        return amount


class CashCalculator(Calculator):
    """Калькулятор для денег."""

    USD_RATE = 73.31
    EURO_RATE = 88.94

    def get_today_cash_remained(self, currency):
        """Выводит сколько дене сегодня осталось или же долг."""
        msg = ""
        # Чтобы не писать if
        currency_dict = {"rub": ("руб", 1),
                         "usd": ("USD", self.USD_RATE),
                         "eur": ("Euro", self.EURO_RATE)}

        today_left = self.get_today_left()

        if today_left == 0:
            msg = "Денег нет, держись"
        elif today_left > 0:
            msg = "На сегодня осталось"
        elif today_left < 0:
            msg = "Денег нет, держись: твой долг -"
        today_left = abs(today_left)

        if today_left:
            name, rate = currency_dict[currency]
            money = today_left/rate
            msg += f" {money:.2f} {name}"

        return msg


class CaloriesCalculator(Calculator):
    """Калькулятор для калорий"""

    def get_calories_remained(self):
        """Выводит сколько можно употребить калорий сегодня."""
        calories_left = self.get_today_left()

        if calories_left <= 0:
            return "Хватит есть!"

        return ("Сегодня можно съесть что-нибудь ещё, но с общей "
                f"калорийностью не более {calories_left} кКал")


class Record:
    def __init__(self, amount, comment, date=None):
        """Принимает и сохраняет аргументы в запись"""
        date_format = "%d.%m.%Y"

        # Если пустая дата, берем сегодня
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()

        self.amount = amount
        self.comment = comment

    def show(self):
        """Тестовый вывод содержимого записи."""
        print("{:>10} | {:<40}|{}".format(self.date.__str__(), self.comment,
              self.amount))


if __name__ == "__main__":

    c = CaloriesCalculator(1000)

    iter = 0
    # Заполнение случайными данными для предварительного тестирования
    while c.get_today_left() >= 0:
        iter += 1

        amount = random.randint(300, 500)
        date = c.get_date(random.randint(0, 3)).strftime("%d.%m.%Y")
        print(f"+{date}: {amount}")
        c.add_record(Record(amount=amount, comment=f"# {iter}", date=date))

        print(c.get_calories_remained())

    c.show_all_records()
    print("За неделю: ", c.get_week_stats())
