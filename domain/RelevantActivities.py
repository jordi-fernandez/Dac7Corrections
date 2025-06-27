from dataclasses import dataclass


@dataclass
class Consideration:
    cons_q1: str
    cons_q2: str
    cons_q3: str
    cons_q4: str


@dataclass
class NumberOfActivities:
    numb_q1: str
    numb_q2: str
    numb_q3: str
    numb_q4: str


@dataclass
class Fees:
    fees_q1: str
    fees_q2: str
    fees_q3: str
    fees_q4: str


@dataclass
class Taxes:
    tax_q1: str
    tax_q2: str
    tax_q3: str
    tax_q4: str


@dataclass
class SaleOfGoods:
    consideration: Consideration
    number_of_activities: NumberOfActivities
    fees: Fees
    taxes: Taxes


@dataclass
class RelevantActivities:
    saleOfGoods: SaleOfGoods


def relevant_activities_from_reportable_seller(reportable_seller: dict):
    goods = reportable_seller['ns2:RelevantActivities']['ns2:SaleOfGoods']
    consideration = Consideration(
        cons_q1=goods['ns2:Consideration']['ns2:ConsQ1']['#text'],
        cons_q2=goods['ns2:Consideration']['ns2:ConsQ2']['#text'],
        cons_q3=goods['ns2:Consideration']['ns2:ConsQ3']['#text'],
        cons_q4=goods['ns2:Consideration']['ns2:ConsQ4']['#text'])

    number_of_activities = NumberOfActivities(
        numb_q1=goods['ns2:NumberOfActivities']['ns2:NumbQ1'],
        numb_q2=goods['ns2:NumberOfActivities']['ns2:NumbQ2'],
        numb_q3=goods['ns2:NumberOfActivities']['ns2:NumbQ3'],
        numb_q4=goods['ns2:NumberOfActivities']['ns2:NumbQ4']
    )

    fees = Fees(
        fees_q1=goods['ns2:Fees']['ns2:FeesQ1']['#text'],
        fees_q2=goods['ns2:Fees']['ns2:FeesQ2']['#text'],
        fees_q3=goods['ns2:Fees']['ns2:FeesQ3']['#text'],
        fees_q4=goods['ns2:Fees']['ns2:FeesQ4']['#text'],
    )
    taxes = Taxes(
        tax_q1=goods['ns2:Taxes']['ns2:TaxQ1']['#text'],
        tax_q2=goods['ns2:Taxes']['ns2:TaxQ2']['#text'],
        tax_q3=goods['ns2:Taxes']['ns2:TaxQ3']['#text'],
        tax_q4=goods['ns2:Taxes']['ns2:TaxQ4']['#text'],
    )

    return RelevantActivities(SaleOfGoods(
        consideration=consideration,
        number_of_activities=number_of_activities,
        fees=fees,
        taxes=taxes
    ))
