import csv
from datetime import datetime, timedelta


# Palauttaa sanakirjassa opiskelijoiden koepisteet muodossa; opiskelijan nimi: korkein suoritus: 
# Jos samaan tehtävänumeroon oppilaalla on useita palautuksia, korkein otetaan huomioon.
# Jos palautus on tehty yli 3 tuntia aloituksen jälkeen, palautusta ei huomioida ollenkaan. 
def viralliset_pisteet():
    with open('palautus.csv') as palautustiedosto, open('tentin_aloitus.csv') as aloitustiedosto:
        aloitukset = {}  # Tänne tallennetaan suoritukset. 
        for rivi in csv.reader(aloitustiedosto, delimiter=';'):  # Luetaan tiedosto ja jaetaan ; - merkin kohdalta tiedoston alkiot. 
            nimi = rivi[0]  #  Nimi on jaon ensimmäinen osa. 
            aika = datetime.strptime(rivi[1], '%H:%M')  # Toisesta osasta luodaan aikaolio. (kellonaika)
            aloitukset[nimi] = aika  # Tallennetaan sanakirjaan. 

        palautukset = {}  # Palautuksista luodaan oma sanakirja. 
        tehtavat = {}  # Tehtävistä luodaan oma sanakirja

        for rivi in csv.reader(palautustiedosto, delimiter=';'):  # Luetaan tiedosto ja jaetaan ; - merkin kohdalta tiedoston alkiot 
            nimi = rivi[0]  # Nimi on jaon ensimmäinen osa. 
            aika = datetime.strptime(rivi[3], '%H:%M')  # Toisesta osasta luodaan aikaolio. 
            if aika < aloitukset[nimi] + timedelta(hours=3):  # Jos aikaolio on pienempi kuin sallittu kokeen suoritusaika:
                if nimi not in tehtavat:  # Jos nimi ei ole tehtävä-sanakirjassa:
                    tehtavat[nimi] = {}  # Lisätään nimi ilman arvoa sanakirjaan. 
                tehtavanro = rivi[1]  # Luodaan muuttuja tehtävänumero johon tallennetaan tehtävänumero tiedostosta. 

                if tehtavanro not in tehtavat[nimi]:  # Jos luotu tehtävänumero ei ole tehtävät-sanakirjassa opiskelijan nimen kohdalla: 
                    tehtavat[nimi][tehtavanro] = int(rivi[2])  # Tallennetaan tehtävänumeroon arvosana. 
                else:
                    if int(rivi[2]) > tehtavat[nimi][tehtavanro]:  # Jos tehtävän pistemäärä on suurempi kuin  sanakirjassa oleva tehtävän pistemäärä:
                        tehtavat[nimi][tehtavanro] = int(rivi[2])  # Korvataan edellinen pistemäärä uudella. 
        
        # Kun sanakirjassa on vain korkeimmat arvosanat per tehtävä jotka on suoritettu aikarajan sisällä:
        # lasketaan loopin avulla suoritettujen tehtävien summa kunkin opiskelijan kohdalla. 
        summa = 0
        for nimi in tehtavat:
            for suoritus, arvosana in tehtavat[nimi].items():
                summa += arvosana
            palautukset[nimi] = summa
            summa = 0
                
        return palautukset


if __name__ == '__main__':

    print(viralliset_pisteet())


