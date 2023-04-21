import matplotlib.pyplot as plt

modszer1 = [10,8,8,11,7,9]
modszer2 = [10,9,4,8,2,8]
kocka = [1,2,3,4,5,6]

plt.plot(kocka,modszer1, label = 'pohar dobas', color = 'g', linestyle = 'dashed' ,marker = 'o', markerfacecolor = 'b' )
plt.plot(kocka,modszer2, label = 'kezbol dobas', color = 'k', marker = 'o', markerfacecolor = 'orange' )
plt.xlabel('Kocka erteke')
plt.ylabel('Hany darab')
plt.title('Kulonbozo dobas minosege')
plt.legend(loc = 'upper right')
plt.show()
