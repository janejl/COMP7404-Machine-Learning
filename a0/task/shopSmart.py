"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """
    "*** YOUR CODE HERE ***"
    totals = [shop.getPriceOfOrder(orderList) for shop in fruitShops]
    return fruitShops[totals.index(min(totals))]

def shopArbitrage(orderList, fruitShops):
    """
    input:
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        maximum profit in amount
    """
    "*** YOUR CODE HERE ***"
    fruit_prices = {}
    for fruit, numPound in orderList:
        fruit_prices[fruit] = [shop.fruitPrices.get(fruit, 0) * numPound for shop in fruitShops]
    max_profit = sum([(max(prices) - min(prices)) for fruit, prices in fruit_prices.items()])
    return max_profit

def shopMinimum(orderList, fruitShops):
    """
    input:
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        Minimun cost of buying the fruits in orderList
    """
    "*** YOUR CODE HERE ***"
    fruit_prices = {}
    for fruit, numPound in orderList:
        fruit_prices[fruit] = [shop.fruitPrices.get(fruit, 0) * numPound for shop in fruitShops]
    return sum([min(prices) for fruit, prices in fruit_prices.items()])

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
  orders = [('apples',3.0)]
  print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())
