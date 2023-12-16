import re
from datefinder import find_dates
from py_pdf_parser.components import PDFDocument
from py_pdf_parser.loaders import load_file
import pandas as pd

def extract(doc:PDFDocument):
    name = []
    fiscal_code = []
    payment_date = []
    retribution_date_dal = []
    retribution_date_al = []
    qualifica = []
    lordo = []
    for page in doc.pages:
        name_and_fiscal_code = [el.text() for el in doc.elements.to_the_right_of(page.elements.filter_by_text_equal("Nome:").extract_single_element())]
        name.append(re.sub(" +", " ", name_and_fiscal_code[0]))
        fiscal_code.append(name_and_fiscal_code[2])

        tmp = []
        for date in find_dates([el.text() for el in doc.elements.to_the_right_of(page.elements.filter_by_text_equal("Data pagamento:").extract_single_element())][0]):
            tmp.append(date.strftime("%d/%m/%Y"))
        payment_date.append(tmp[0])

        tmp = []
        for date in find_dates(page.elements.filter_by_text_contains("Retribuzione").extract_single_element().text()):
            tmp.append(date.strftime("%d/%m/%Y"))
        retribution_date_dal.append(tmp[0])
        retribution_date_al.append(tmp[1])

        qualifica.append([el.text() for el in doc.elements.to_the_right_of(page.elements.filter_by_text_equal("Qualifica:").extract_single_element())][0])
        lordo.append([el.text() for el in doc.elements.to_the_right_of(page.elements.filter_by_text_equal("LORDO").extract_single_element())][0])
    return name, fiscal_code, payment_date, retribution_date_dal, retribution_date_al, qualifica, lordo

def main():
    doc = load_file("./Dataset/Buste_1_3.pdf")
    name, fiscal_code, payment_date, retribution_date_dal, retribution_date_al, qualifica, lordo = extract(doc)
    data = {
        "nome": name,
        "codice_fiscale": fiscal_code, 
        "data_pagamento": payment_date,
        "data_retribuzione_dal": retribution_date_dal,
        "data_retribuzione_al": retribution_date_al,
        "qualifica": qualifica,
        "lordo": lordo
    }
    df = pd.DataFrame(data=data)
    print(df)

if __name__ == "__main__":
    main()