def kaina_red(price):
    kaina=""
    for i in price:
        try:
            i = int(i)
        except:
            pass
        if type(i) == int:
            i = str(i)
            kaina = kaina + i
        elif i == ',':
            kaina = kaina + i
    try:
        kaina = int(kaina)
    except:
        kaina = kaina.replace(',', '.')
        kaina = round(float(kaina))
        kaina = int(kaina)
    return kaina
