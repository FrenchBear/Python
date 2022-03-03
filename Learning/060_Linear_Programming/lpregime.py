# Another example of linear programming
# From '50 clés pour comprendre les maths', §45
#
# 2019-04-24 PV
#
# Two products can be used for a regime, Solido and Liquidex
# Each provide Vitamines and Minerals:
#             Solido (2€)  Liquidex (7€)       Needs
# Vitamins      2 mg           3 mg            120 mg
# Minerals     10 mg          50 mg            880 mg
#
# What are the optimal counts of Solido and Liquidex to buy to achiee the needs?

#from pulp import LpProblem, LpVariable, LpMinimize
import pulp     # type: ignore

problem = pulp.LpProblem("regime", pulp.LpMinimize)

# price per product (unit)
s_p = 2
l_p = 7

# contribution of each product
v_s = 2
v_l = 3
m_s = 10
m_l = 50

# target
v_t = 120
m_t = 880

# count variables (solido_count and liquidex_count)
s_c = pulp.LpVariable("s_c", 0, 1000, 'Integer')
l_c = pulp.LpVariable("l_c", 1, 1000, 'Integer')

# Contraints
problem += s_c*v_s + l_c*v_l >= v_t
problem += s_c*m_s + l_c*m_l >= m_t

# Objective (total price)
problem += s_c*s_p + l_c*l_p

print(problem)

problem.solve()

print('Solido:  ', pulp.value(s_c))
print('Liquidex:', pulp.value(l_c))
