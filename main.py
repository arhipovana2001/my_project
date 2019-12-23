import matplotlib.pyplot as plt
import numpy as np

with open('input.txt', 'r', encoding='utf-8') as input_file:
    inp = input_file.read().splitlines()

QD_str = inp[0]
QD_str = QD_str.replace(',', '.')
QS_str = inp[1]
QS_str = QS_str.replace(',', '.')
keyword_str = inp[2]
tax_str = inp[3]
tax_str = tax_str.replace(',', '.')
QS_elements = []
QD_elements = []
balance = []
QD_0 = []

QD = QD_str[QD_str.find(' ') + 1:]  #разбиение функции на элементы и занесение их в список
QD = QD[QD.find(' ') + 1:]
symbolD = QD.find('+')
if symbolD == -1:
    symbolD = QD.find('-')
elmnt1 = QD[:symbolD]
elmnt2 = QD[symbolD:]
QD_elements.append(elmnt1)
QD_elements.append(elmnt2)

QS = QS_str[QS_str.find(' ') + 1:]
QS = QS[QS.find(' ') + 1:]
symbolS = QS.find('+')
if symbolS == -1:
    symbolS = QS.find('-')
elmnt3 = QS[:symbolS]
elmnt4 = QS[symbolS:]
QS_elements.append(elmnt3)
QS_elements.append(elmnt4)

for i in range(0, 2):
    el = QD_elements[i]
    if el[0] == '-':
        el = el.replace('-', '+')
    elif el[0] != '-':
        el = '-' + el
    QD_0.append(el)

print('QD_elements =', QD_elements)
print('QS_elements =', QS_elements)


def price(d, s):
    """Calculation and display of the market price"""
    q1 = float(d[0])
    q2 = float(s[0])
    Q = q1 + q2
    p1 = float(s[1][:s[1].find('P')])
    p2 = float(d[1][:d[1].find('P')])
    P = p1 + p2
    balance_price = (-Q) / P
    balance.append(balance_price)
    print('P =', format(balance_price, '.2f'))


def volume(p, qs):
    """Calculation and display of the market volume"""
    balance_volume = float(qs[0])
    coefficient = qs[1]
    coefficient = float(coefficient[:coefficient.find('P')])
    balance_volume = balance_volume + coefficient * balance[0]
    print('Q =', format(balance_volume, '.2f'))
    balance.append(balance_volume)


print('Начальное равновесие:')
price(QD_0, QS_elements)
volume(balance[0], QS_elements)
balance = []
print('Новое равновесие:')

if keyword_str == 'налог':
    t = float(tax_str[:tax_str.find('%')])
    QD_1_elements = QD_elements
    QS_1_elements = []
    QS_1_elements.append(QS_elements[0])
    price_new = QS_elements[1][0] + str((1 - t / 100) * int(QS_elements[1][1:QS_elements[1].find('P')]))
    QS_1_elements.append(str(price_new) + 'P')
    price(QD_0, QS_1_elements)
    volume(balance[0], QS_1_elements)
elif keyword_str == 'субсидия':
    t = float(tax_str[:tax_str.find('%')])
    QD_1_elements = QD_elements
    QS_1_elements = []
    QS_1_elements.append(QS_elements[0])
    price_new = QS_elements[1][0] + str(1 + t / 100) * int(QS_elements[1][1:QS_elements[1].find('P')])
    QS_1_elements.append(str(price_new) + 'P')
    price(QD_0, QS_1_elements)
    volume(balance[0], QS_1_elements)

fig, qs = plt.subplots()
x = np.linspace(0, int(QD_elements[0]), 10)
y = (float(QD_elements[0]) - x) / (-(float(QD_elements[1][:QD_elements[1].find('P')])))
qs.plot(x, y, color='red', linewidth=2)

x = np.linspace(0, float(QD_elements[0]) / -(float(QD_elements[1][:QD_elements[1].find('P')])), 10)
y = (x - (-float((QS_elements[0])))) / float(QS_elements[1][:QS_elements[1].find('P')])
qs.plot(x, y, color='green', linewidth=2)

leg1 = 'D'
leg2 = 'S'
plt.legend((leg1, leg2), frameon=False, loc='best')  #remove the frame of the legend
plt.title('Рыночное равновесие')
plt.xlabel('Q')
plt.ylabel('P')
plt.show()
