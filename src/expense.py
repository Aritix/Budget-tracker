from entry import Entries, Entry
from reference import References, Reference
import datetime
import matplotlib.pyplot as plt
import numpy as np
from constantes import YEAR
from constantes import CURRENCY


class Expenses:
    default_class = "Autres"

    def __init__(self, default_class="Autres"):
        self.default_class = default_class
        self.sums = {default_class: 0}
        self.time_sums = {}
        self.time_min = None
        self.time_max = None

    def add_expense(self, entry: Entry, category_name: str = default_class):
        day = entry.day
        month = entry.month
        self.sums[category_name] = entry.price + (
            self.sums[category_name] if category_name in self.sums.keys() else 0
        )
        temp_key = (day, month)
        if category_name in self.time_sums.keys():
            self.time_sums[category_name].append(((day, month), entry.price))
        else:
            self.time_sums[category_name] = [((day, month), entry.price)]
        if self.time_min != None:
            self.time_min = min(
                self.time_min,
                datetime.datetime.strptime(f"{YEAR}-{month}-{day}", "%Y-%m-%d"),
            )
        else:
            self.time_min = datetime.datetime.strptime(
                f"{YEAR}-{month}-{day}", "%Y-%m-%d"
            )
        if self.time_max != None:
            self.time_max = max(
                self.time_max,
                datetime.datetime.strptime(f"{YEAR}-{month}-{day}", "%Y-%m-%d"),
            )
        else:
            self.time_max = datetime.datetime.strptime(
                f"{YEAR}-{month}-{day}", "%Y-%m-%d"
            )

    def show_by_category(self):
        str_res = ""
        for category, amount in self.sums.items():
            str_res += f"{category}, {amount}\n"
        return str_res

    def time_graph(self, subplot=None, SavedFileName=None, show=False):
        labels = self.time_sums.keys()
        items = sum([self.time_sums[label] for label in labels], [])
        times = [tpl[0] for tpl in items]
        times = [
            datetime.datetime.strptime(f"{YEAR}-{tpl[1]}-{tpl[0]}", "%Y-%m-%d")
            for tpl in times
        ]
        bottom_dict = {}
        for time in times:
            bottom_dict[time] = 0
        ax = plt.subplot(111) if subplot == None else subplot
        for category_name, list_expenses in self.time_sums.items():
            times = [
                datetime.datetime.strptime(
                    f"{YEAR}-{tpl[0][1]}-{tpl[0][0]}", "%Y-%m-%d"
                )
                for tpl in list_expenses
            ]
            amounts = [tpl[1] for tpl in list_expenses]
            # Listes aggrégées pour fusionner les dépenses de même catégorie à la même date.
            times_agg = []
            amounts_agg = []
            for time, amount in zip(times, amounts):
                if time in times_agg:
                    amounts_agg[times_agg.index(time)] += amount
                else:
                    times_agg.append(time)
                    amounts_agg.append(amount)
            bottom = [bottom_dict[time] for time in times_agg]
            ax.bar(times_agg, amounts_agg, label=category_name, bottom=bottom)
            for time, amount in zip(times_agg, amounts_agg):
                bottom_dict[time] += amount

        ax.grid()
        ax.set_title(
            f"Dépense du {self.time_min.strftime("%m/%d")} au {self.time_max.strftime("%m/%d")}"
        )
        ax.legend()
        ax.set_xlabel("Date")
        ax.set_ylabel(f"Montant ({CURRENCY})")
        if SavedFileName:
            plt.savefig(SavedFileName)
        else:
            if show:
                plt.show()

    def pie_graph(self, subplot=None, SavedFileName=None, show=False):
        labels = self.sums.keys()
        amounts = [(self.sums[name] if self.sums[name] >= 0 else 0) for name in labels]
        ax = plt.subplot(111) if subplot == None else subplot

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                # return "{p:.2f}%  ({v:d}{c})".format(p=pct, v=val, c=" " + CURRENCY)
                return f"{val:d}"

            return my_autopct

        ax.pie(amounts, labels=labels, autopct=make_autopct(amounts))  #'%.1f')
        if SavedFileName:
            plt.savefig(SavedFileName)
        else:
            if show:
                plt.show()

    def all_graph(self, SavedFileName=None, show=False):
        plt.figure(figsize=(15, 6))
        self.pie_graph(plt.subplot(121), show=False)
        self.time_graph(plt.subplot(122), show=False)
        if SavedFileName:
            plt.savefig(SavedFileName)
        else:
            if show:
                plt.show()

    def __str__(self):
        return f"<Expenses object with total amount of {sum(self.sums.values())}>"
