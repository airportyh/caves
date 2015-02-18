import xlrd
import re

def parse_numbers(s):
  numbers = []
  for part in re.split('[,./ ]', s):
    part = part.strip()
    if part == '':
      continue
    m = re.search('-', part)
    if m is not None:
      start_range = int(part[0:m.start()])
      end_range = int(part[m.start()+1:len(part)])
      i = start_range
      while i <= end_range:
        numbers.append(i)
    else:
      numbers.append(int(part))
  return numbers

def all_numbers(lst):
  if type(lst) != list:
    return False
  for n in lst:
    if type(n) != int:
      return False
  return True

book = xlrd.open_workbook('cloister caves.xls')
sheet = book.sheet_by_index(0)

col_offset = 2
i = 0
locations = []
while i < 15:
  name = sheet.cell(0, col_offset + i).value
  locations.append({
    'name': name,
    'col_idx': col_offset + i
  })
  i = i + 1

row_offset = 3
artifacts = []
i = 0
while i < 176:
  artifact_name = sheet.cell(row_offset + i, 0)
  artifact_chinese_name = sheet.cell(row_offset + i, 1)
  artifacts.append({
    'name': artifact_name.value,
    'chinese_name': artifact_chinese_name.value,
    'row_idx': row_offset + i
  })
  i = i + 1

for artifact in artifacts:
  for location in locations:
    cell = sheet.cell(artifact['row_idx'], location['col_idx'])
    if cell.ctype != xlrd.XL_CELL_EMPTY:
      if cell.ctype == xlrd.XL_CELL_NUMBER:
        numbers = "{:0.0f}".format(cell.value)
      else:
        numbers = cell.value
        numbers = numbers.replace(u'\xef\xbc\x8c', u',')
        numbers = numbers.replace(u'\uff0c', u',')
      numbers = parse_numbers(numbers)
      assert all_numbers(numbers)
      print "These caves have a", artifact['name'], "in in the", location['name'], ":", numbers
      
      