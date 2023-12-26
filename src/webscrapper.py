import urllib.request
import ssl

context = ssl._create_unverified_context()
#urllib.request.urlopen(req,context=context)

x = 0
while x <= 20 :
    fp = urllib.request.urlopen(f"https://www.police.hu/hu/hirek-es-informaciok/utinfo/baleseti-hirek?field_feltolto_szerv_target_id=All&page={str(x)}", context=context)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    print(mystr)
    with open("baleset.html", "w", encoding="utf-8") as page:
        page.write(mystr)
    x=+1



"""
fp = urllib.request.urlopen("https://www.police.hu/hu/hirek-es-informaciok/utinfo/baleseti-hirek", context=context)


mybytes = fp.read()
mystr = mybytes.decode("utf8")
fp.close()
print(mystr)
with open("baleset.html", "w", encoding="utf-8") as page:
    page.write(mystr)
"""