# Clovece nehnevaj sa, projekt pre predmet programovanie 1 na FEI STU v roku 2021.
# Pravidla hry:
# Pravidla su trosku zjednodusene,hra je tym padom sviznejsia a jednoduchsia.
# 1. Nie je potrebne hodit 6 aby si hrac vlozil prvu figurku na hraciu.
# 2. Vyhadzovanie nie je mozne,preferujem hru,pri ktorej sa naozaj nik nebude hnevat
# 3. Ak hrac hodi na hracej kocke cislo 6,hadze znova,toto je mozne najviac trikrat.
# 5. Figurka je automaticky z pred domcekov presunuta na posledny volny domcek
# 4. Vyhrava hrac,ktory dostane vsetky svoje figurky do domcekov ako prvy.
########################################################################################################################

# pouzite kniznice
import random

# globalne premenne
# pocitadlo figuriek v domcekoch
v_domceku0 = 0
v_domceku1 = 0
v_domceku2 = 0
v_domceku3 = 0
# celkovy pocet figuriek
pocet_figuriek = 0

# Funkcia, ktora ziskava korektnu velkost plochy od uzivatela


def get_velkost_plochy():
    min_hodnota = 5
    while True:
        n = input('Zadajte neparne cislo vacsie ako ' + str(min_hodnota) + ':')
        if n[0] in ('+', '-') and n[1:].isdigit() or n.isdigit():                               # n musi byt cele cislo

            n = int(n)

        else:

            print('Vstupna hodnota musi byt cele cislo,prosim zadajte inu hodnotu.')
            continue
        if n < 5:                                                                              # n musi byt vacsie ako 5

            print('Vstupna hodnota je mensia ako ', min_hodnota, ',prosim zadajte inu hodnotu.')
            continue
        if n % 2 == 0:     # n musi byt neparne cislo

            print('Vstupna hodnota je parne cislo,prosim zadajte inu hodnotu.')
            continue
        break
    return n


# Funkcia sa stara o generovanie plochy,je to list,do ktoreho su na zaklade suradnic pridavane znaky na urcite miesta


def gen_plochu(vel):
    stred = int(vel / 2)
    plocha = list()
    for i in range(vel):

        plocha.append(list())
        for j in range(1 + vel):

            if i == stred and j == stred:

                plocha[i].append('X')
                continue
            if i == stred and j not in (0, vel - 1):

                plocha[i].append('0')
                continue
            if j == stred and i not in (0, vel - 1):

                plocha[i].append('0')
                continue
            if j in (stred - 1, stred, stred + 1):

                plocha[i].append('*')
                continue
            if i in (stred - 1, stred, stred + 1):

                plocha[i].append('*')
                continue
            plocha[i].append(' ')

    return plocha

# Funkcia nam tlaci plochu aj s figurkami  do konzoly, je do nej predavany vystup z funkcie gen_plochu.


def tlac_plochu(plocha, figurky0, figurky1, figurky2, figurky3):

    for i in range(len(plocha)):
        for j in range(len(plocha)):

            # tuto su figurky tlacene na prazdnu plochu na zaklade ich suradnic
            if [i, j] in figurky0:

                print('A', end=' ')
            elif [i, j] in figurky1:

                print('B', end=' ')
            elif [i, j] in figurky2:

                print('C', end=' ')
            elif [i, j] in figurky3:

                print('D', end=' ')
            else:

                print(plocha[i][j], end=' ')
        print()

# Tato funkcia generuje ((n - 3) / 2) figuriek pre kazdeho hraca


def gen_figurky(hrac, vel):
    global pocet_figuriek
    pocet_figuriek = int((vel - 3) / 2)
    # figurky su umiestnovane mimo hracej plochy,az vo funkcii pohyb sa pridavaju  na plochu.
    figurky = list()
    if hrac == 0:

        zaciatok = [0, int((vel / 2) + 2)]
    elif hrac == 1:

        zaciatok = [vel-1, int((vel / 2) - 2)]
    elif hrac == 2:

        zaciatok = [int((vel / 2) + 2), vel-1]
    elif hrac == 3:

        zaciatok = [int((vel / 2) - 2), 0]
    for i in range(pocet_figuriek):

        figurky.append(zaciatok.copy())

    return figurky

# Funkcia nam ziskava hodnotu od 1 do 6 vyuzitim kniznice random


def get_kocka(hody=None):
    if not hody:

        hody = []
    hody.append(random.randint(1, 6))
    if len(hody) < 3 and hody[-1] == 6:  # je osetrene aby hrac nemohol hodit cislo 6 viac ako trikrat.

        return get_kocka(hody)
    return sum(hody)

# Funkcia ma na starosti pohyb figuriek,je asi najviac komplexna zo vsetkych mojich funkcii
# Hracia plocha je od stredu rozdelena na "kvadranty",zistuje sa kde sa figurka nachadza
# Podla polohy figurky vieme po ktorej osi sa figurka potrebuje posunut
# Figurka je zoznam so svojou suradnicou X [0] a Y [1]


def pohyb(kocka, figurka, vel, hrac, prejdene):
    global v_domceku0, v_domceku1, v_domceku2, v_domceku3
    stred = int(vel / 2)
    # presuvanie novej figurky na start
    if hrac == 0 and prejdene == 0:

        figurka[0] = 0
        figurka[1] = stred + 1
    elif hrac == 1 and prejdene == 0:

        figurka[0] = vel-1
        figurka[1] = stred-1
    elif hrac == 2 and prejdene == 0:

        figurka[0] = stred+1
        figurka[1] = vel-1
    elif hrac == 3 and prejdene == 0:

        figurka[0] = stred-1
        figurka[1] = 0

    prejdene += kocka

    if prejdene >= (int(vel * 4) - 5):           # celkova cesta figurky,aby bola figurka nutena zastavit pred domcekom

        prejdene = 0
        # presuvanie figuriek do domceka ak stoja na poslednom policku
        if hrac == 0:

            figurka[0] = stred - 1 - v_domceku0
            figurka[1] = stred
            v_domceku0 += 1

        elif hrac == 1:

            figurka[0] = stred + 1 + v_domceku1
            figurka[1] = stred
            v_domceku1 += 1

        elif hrac == 2:

            figurka[0] = stred
            figurka[1] = stred + 1 + v_domceku2
            v_domceku2 += 1

        elif hrac == 3:

            figurka[0] = stred
            figurka[1] = stred - 1 - v_domceku3
            v_domceku3 += 1

    else:
        # Tu sa zistuje poloha figutky podla Y a X suradnice a nasledne sa posuva po potrebnej osi
        for i in range(kocka):

            if figurka[0] == 0 and figurka[1] == stred:

                figurka[1] += 1

            elif figurka[0] == (vel - 1) and figurka[1] == stred:

                figurka[1] -= 1

            elif figurka[0] == stred and figurka[1] == 0:

                figurka[0] -= 1

            elif figurka[0] == stred and figurka[1] == (vel - 1):

                figurka[0] += 1

            elif figurka[0] < stred and figurka[1] < stred:  # vlavo hore

                if figurka[1] == (stred - 1) and not figurka[0] == 0:

                    figurka[0] -= 1

                elif figurka[0] == (stred - 1) and not figurka[1] == (stred - 1):

                    figurka[1] += 1

                elif figurka[0] == 0 and figurka[1] == (stred - 1):

                    figurka[1] += 1

            elif figurka[0] > stred and figurka[1] > stred:  # vpravo dole

                if figurka[1] == (stred + 1) and not figurka[0] == (vel - 1):

                    figurka[0] += 1

                elif figurka[0] == (stred + 1) and not figurka[1] == (stred + 1):

                    figurka[1] -= 1

                elif figurka[1] == (stred + 1) and figurka[0] == (vel - 1):

                    figurka[1] -= 1

            elif figurka[0] < stred and figurka[1] > stred:  # vpravo hore

                if figurka[1] == (stred + 1) and not figurka[0] == (stred - 1):

                    figurka[0] += 1

                elif figurka[0] == (stred - 1) and not figurka[1] == (vel - 1):

                    figurka[1] += 1

                elif figurka[1] == (vel - 1) and figurka[0] == (stred - 1):

                    figurka[0] += 1

            elif figurka[0] > stred and figurka[1] < stred:         # vlavo dole

                if figurka[1] == (stred - 1) and not figurka[0] == (stred + 1):

                    figurka[0] -= 1

                elif figurka[0] == (stred + 1) and not figurka[1] == 0:

                    figurka[1] -= 1

                elif figurka[0] == (stred + 1) and figurka[1] == 0:

                    figurka[0] -= 1

    return prejdene

# Funkcia kontroluje,ze ci uz nejaky hrac ma v domcekoch vsetky svoje figurky


def skontroluj_vyhru(v_domceku, hrac):
    if v_domceku == pocet_figuriek:

        # Ak vyhral hrac A ->65=A v ascii, hrac B -> 66=B v ascii, hrac C -> 67=C, hrac D -> 68=D

        print("Vyhral Hrac ", chr(hrac + 65))
        return True
    return False

# Hlavna funkcia, v ktorej su volane vsetky predosle,ktore boli vytvorene


def main():
    global v_domceku0, v_domceku1, v_domceku2, v_domceku3

    vel = get_velkost_plochy()
    prejdene0 = 0
    prejdene1 = 0
    prejdene2 = 0
    prejdene3 = 0
    figurky0 = gen_figurky(0, vel)
    figurky1 = gen_figurky(1, vel)
    figurky2 = gen_figurky(2, vel)
    figurky3 = gen_figurky(3, vel)
    plocha = gen_plochu(vel)
    input("Stlacte Enter na zahajenie simulacie:")

    while 1 == 1:
        kocka = get_kocka(hody=None)
        print("Hrac A hodil:", kocka)
        prejdene0 = pohyb(kocka, figurky0[v_domceku0], vel, 0, prejdene0)
        tlac_plochu(plocha, figurky0, figurky1, figurky2, figurky3)
        if skontroluj_vyhru(v_domceku0, 0):
            break

        kocka = get_kocka(hody=None)
        print("Hrac B hodil:", kocka)
        prejdene1 = pohyb(kocka, figurky1[v_domceku1], vel, 1, prejdene1)
        tlac_plochu(plocha, figurky0, figurky1, figurky2, figurky3)
        if skontroluj_vyhru(v_domceku1, 1):
            break

        kocka = get_kocka(hody=None)
        print("Hrac C hodil:", kocka)
        prejdene2 = pohyb(kocka, figurky2[v_domceku2], vel, 2, prejdene2)
        tlac_plochu(plocha, figurky0, figurky1, figurky2, figurky3)
        if skontroluj_vyhru(v_domceku2, 2):
            break

        kocka = get_kocka(hody=None)
        print("Hrac D hodil:", kocka)
        prejdene3 = pohyb(kocka, figurky3[v_domceku3], vel, 3, prejdene3)
        tlac_plochu(plocha, figurky0, figurky1, figurky2, figurky3)
        if skontroluj_vyhru(v_domceku3, 3):
            break


main()
input()
