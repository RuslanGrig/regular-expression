from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

out_list = []
names_list = []
for contact in contacts_list:
    name = re.findall(r'\w+', ' '.join(contact[:3]))
    name_correct = [x.lower().capitalize() for x in name]
    for i in range(len(name_correct)):
       contact[i] = name_correct[i]
    name_correct_str = ' '.join(contact[:2])
    if name_correct_str in names_list:   
        index = names_list.index(name_correct_str)
        for x in range(2, len(out_list[index])):
           if not out_list[index][x]:
              out_list[index][x] = contact[x]
    else:
       names_list.append(name_correct_str)
       out_list.append(contact)

pattern = (
    r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'\
    r'(?:\s*\(?(?:доб\.?)\s*(\d+)\)?)?')
subst = r'+7(\2)\3-\4-\5'
subst_ext = r'+7(\2)\3-\4-\5 доб.\6'

for i, phone in enumerate(out_list):
    if phone[5]:  
        res_search = re.search(pattern, phone[5])  
        if res_search:
            if res_search.group(6):
                out_list[i][5] = re.sub(pattern, subst_ext, out_list[i][5])
            else:
                out_list[i][5] = re.sub(pattern, subst, out_list[i][5])

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
    datawriter.writerows(out_list)