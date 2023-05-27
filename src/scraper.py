import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

currdir = os.getcwd()
service = Service(os.path.join(currdir, 'chromrdriver.exe'))
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://sirup.lkpp.go.id/sirup/ro/rekap/klpd/D5')

try:
    rekap = []
    table = WebDriverWait(driver, 10) \
        .until(EC.visibility_of_element_located((By.ID, 'rekapKldi')))
    trs = table.find_elements(By.XPATH, './/tbody//tr')

    for tr in trs:
        tds = tr.find_elements(By.XPATH, './/td')

        # satuan kerja -----------------------
        pa_text = tds[1].find_element(By.TAG_NAME, 'a').text
        satuan_kerja = tds[1].text.replace(pa_text, '')

        # peyedia ----------------------------
        peyedia_paket = tds[2].text  # paket
        peyedia_pagu = tds[3].text  # pagu

        # swakelola --------------------------
        swakelola_paket = tds[4].text  # paket
        swakelola_pagu = tds[5].text  # pagu

        data = {
            'satuan_kerja': satuan_kerja,
            'penyedia': {
                'paket': peyedia_paket,
                'pagu': peyedia_pagu,
            },
            'swakelola': {
                'paket': swakelola_paket,
                'pagu': swakelola_pagu,
            }
        }

        rekap.append(data)
    print(rekap)

    # save as json file
    with open('result.json', 'w') as fp:
        json.dump(rekap, fp)

finally:
    driver.quit()
