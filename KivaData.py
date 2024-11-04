import time

import requests
import pandas as pd
from dateutil import parser
import datetime
import csv
import json
import xlsxwriter
import pathlib

# base_url = 'https://api.kivaws.org/graphql?query='
base_url = 'https://api.kivaws.org/graphql?query='

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36"
}


STARTING_DATE_ONE = datetime.datetime(2023, 9, 1)
ENDING_DATE_ONE = datetime.datetime(2024, 9, 1)

DATA_LIST = []
ID_SET = set()


def fetchIDS(startingDate, endingDate):
    offset = 28000
    id_count = 0
    while True:
        graphql_query = f'{{lend {{loans(offset: {offset}, limit:100, sortBy: newest, filters:{{status:all}})' \
                        f'{{totalCount values {{id fundraisingDate plannedExpirationDate}}}}}}}}'
        r = requests.get(base_url + graphql_query, headers=headers)
        print(r.status_code)
        r = r.json()
        print(r['data']['lend']['loans']['totalCount'])
        print(offset)
        if not r['data']['lend']['loans']['values']:
            break
        data = r['data']['lend']['loans']['values']
        first_val = data[0]
        first_fundraising_date = first_val['fundraisingDate']
        parsed_first_fundraising_date = parser.parse(first_fundraising_date)
        totalCount = r['data']['lend']['loans']['totalCount']
        while totalCount not in [i for i in range(2700000, 2900000)]:
            print("retrying...")
            graphql_query = f'{{lend {{loans(offset: {offset}, limit:100, sortBy: newest, filters:{{status:all}})' \
                            f'{{totalCount values {{id fundraisingDate plannedExpirationDate}}}}}}}}'
            r = requests.get(base_url + graphql_query, headers=headers)
            print(r.status_code)
            r = r.json()
            print(r['data']['lend']['loans']['totalCount'])
            totalCount = r['data']['lend']['loans']['totalCount']
            print(offset)
            if not r['data']['lend']['loans']['values']:
                break
            data = r['data']['lend']['loans']['values']
            first_val = data[0]
            first_fundraising_date = first_val['fundraisingDate']
            parsed_first_fundraising_date = parser.parse(first_fundraising_date)
        if parsed_first_fundraising_date.date() < startingDate.date():
            break
        for value in data:
            id = value['id']
            fundraising_date = value['fundraisingDate']
            planned_expiration_date = value['plannedExpirationDate']
            parsedFundraisingDate = parser.parse(fundraising_date)
            if planned_expiration_date is None:
                print("Continue...")
                continue
            parsedPlannedExpirationDate = parser.parse(planned_expiration_date)
            if startingDate.date() <= parsedFundraisingDate.date() <= endingDate.date() \
                    and (parsedPlannedExpirationDate.date() - parsedFundraisingDate.date()).days in [35,
                                                                                                     36]:  # check if it's 35, 36 due to rounding error using .date()

                old_length = len(ID_SET)
                ID_SET.add(id)
                if len(ID_SET) != old_length:
                    id_count += 1
                    print("id added", id_count, id, fundraising_date, planned_expiration_date)
                else:
                    print("Not a unique id")
            else:
                print(parsedFundraisingDate.date() >= startingDate.date())
                print(parsedPlannedExpirationDate.date() <= endingDate.date())
                print((parsedPlannedExpirationDate.date() - parsedFundraisingDate.date()).days)
                print("id not added", id_count, fundraising_date, planned_expiration_date)
        offset += 100


def write_IDS(id_list):
    with open("LoanIDs.csv", mode='w') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(id_list)
        print("done writing.")
        print(len(id_list))


def get_data():
    offset = 0

    try:
        with open("LoanIDs.csv", mode='r') as file:
            id_list = [int(val) for val in list(csv.reader(file))[0]]
            print("Loaded in ids")
    except FileNotFoundError:
        fetchIDS(STARTING_DATE_ONE, ENDING_DATE_ONE)
        id_list = list(ID_SET)
        write_IDS(id_list)

    print("number of ids", len(id_list))
    slice_beginning = 0
    slice_ending = 100
    print(id_list)

    while slice_beginning < len(id_list):
        print(slice_beginning, len(id_list))
        graphql_query = f'{{lend {{ loans(offset:{offset}, limit:100, filters:{{loanIds:{id_list[slice_beginning:slice_ending]}, status: all}}) {{values {{id name borrowerCount geocode {{country {{isoCode}}}} originalLanguage {{ isoCode }} ' \
                        f'... on LoanPartner {{partnerId partnerName partner {{ riskRating}} }} activity {{ name }} description descriptionInOriginalLanguage sector {{ name }} loanAmount fundraisingDate plannedExpirationDate raisedDate loanFundraisingInfo {{ fundedAmount }}' \
                        f'status use disbursalDate gender distributionModel repaymentInterval lenderRepaymentTerm ' \
                        f'lenders {{totalCount}} lendingActions{{totalCount}} }} }} }} }}'
        r = requests.get(base_url + graphql_query, headers=headers)
        print(r.status_code)
        r = r.json()
        print(id_list[slice_beginning:slice_ending])
        data = r['data']['lend']['loans']['values']
        print(len(data))
        for value in data:
            temp_lst = []
            lenders_list = []
            lendingActionOffset = 0
            loan_id = value['id']

            totalCountLendingActions = value['lendingActions']['totalCount']
            while lendingActionOffset < totalCountLendingActions:
                try:
                    graphql_query_2 = f'{{lend {{loans(filters: {{loanIds: {[loan_id]}, status: all }}) {{values {{lendingActions(offset:{lendingActionOffset}, limit: 100){{totalCount values {{ shareAmount latestSharePurchaseDate lender {{publicId name loanCount inviteeCount' \
                                      f' lenderPage {{country {{isoCode}} loanBecause occupation }} }} }} }} }} }} }} }}'
                    r2 = requests.get(base_url + graphql_query_2, headers=headers, timeout=300)
                    print(loan_id, r2.status_code)
                    r2 = r2.json()
                    if r2 is None:
                        break
                    lendingActionData = r2['data']['lend']['loans']['values'][0]['lendingActions']['values']
                    lenders_list.extend(lendingActionData)
                    print("lending action", lendingActionOffset)
                    lendingActionOffset += 100
                except Exception as e:
                    print(e)
                    print("reattempting due to timeout error...")
                    time.sleep(5)
                    continue

            print("Done with lending actions...")
            loan_name = value['name']
            borrower_count = value['borrowerCount']
            loan_country = value['geocode']['country']['isoCode'] if value['geocode'] is not None and \
                                                                     value['geocode'][
                                                                         'country'] is not None else "Null"
            original_language = value['originalLanguage']['isoCode']
            partner_id = value['partnerId'] if "partnerId" in value else "Null"
            partner_name = value['partnerName'] if "partnerName" in value else "Null"
            partner_risk_rating = value['partner']['riskRating'] if 'partner' in value else "Null"
            activity = value['activity']['name']
            description = value['description']
            descriptionOriginal = value['descriptionInOriginalLanguage']
            sector = value['sector']['name']
            loan_amount = value['loanAmount']
            fundraising_date = value['fundraisingDate']
            planned_expiration_date = value['plannedExpirationDate']
            raised_date = value['raisedDate'] if value['raisedDate'] is not None else "Null"
            funded_amount = value['loanFundraisingInfo']['fundedAmount']
            status = value['status']
            use = value['use']
            disbursal_date = value['disbursalDate']
            gender = value['gender']
            distribution_model = value['distributionModel']
            repayment_interval = value['repaymentInterval']
            lender_repayment_term = value['lenderRepaymentTerm']
            lender_count = value['lenders']['totalCount']
            lenders = lenders_list

            temp_lst.extend(
                [loan_id, loan_name, borrower_count, loan_country, gender, original_language, partner_id,
                 partner_name, partner_risk_rating, description,
                 descriptionOriginal, sector, activity, loan_amount, fundraising_date,
                 planned_expiration_date,
                 raised_date, funded_amount, status, use, disbursal_date, distribution_model,
                 repayment_interval,
                 lender_repayment_term, lender_count, lenders])
            DATA_LIST.append(temp_lst)

        slice_beginning += 100
        slice_ending += 100
    print(len(DATA_LIST))

    df = pd.DataFrame(DATA_LIST, columns=["LOAN_ID", "LOAN_NAME", "BORROWER COUNT", "LOAN COUNTRY", "GENDER",
                                          "ORIGINAL_LANGUAGE",
                                          "PARTNER ID", "PARTNER NAME", "PARTNER RISK RATING", "DESCRIPTION",
                                          "DESCRIPTION IN ORIGINAL LANGUAGE",
                                          "SECTOR", "ACTIVITY", "LOAN AMOUNT", "FUNDRAISING DATE",
                                          "PLANNED EXPIRATION DATE",
                                          "DATE RAISED", "FUNDED AMOUNT", "STATUS", "USE", "DISBURSAL DATE",
                                          "DISTRIBUTION MODEL",
                                          "REPAYMENT INTERVAL", "LENDER TERM", "LENDER COUNT", "LENDERS"])

    df.to_excel("kiva_data_sept_2023_2024.xlsx", engine='xlsxwriter')
    print(df)


def main():
    get_data()
    print("Success!")


main()
