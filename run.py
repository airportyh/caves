import xlrd
import re
import sys

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

def cave_numbers_for_cell(cell):
  if cell.ctype != xlrd.XL_CELL_EMPTY:
    if cell.ctype == xlrd.XL_CELL_NUMBER:
      numbers = "{:0.0f}".format(cell.value)
    else:
      numbers = cell.value
      numbers = numbers.replace(u'\xef\xbc\x8c', u',')
      numbers = numbers.replace(u'\uff0c', u',')
    numbers = parse_numbers(numbers)
    assert has_all_numbers(numbers)
    return numbers
  else:
    return []

def has_all_numbers(lst):
  if type(lst) != list:
    return False
  for n in lst:
    if type(n) != int:
      return False
  return True

if len(sys.argv) < 2:
  print "Usage: python run.py <excel file>"
  sys.exit()

def read_file(filename):
  book = xlrd.open_workbook(filename, formatting_info=True)
  sheet = book.sheet_by_index(0)
  
  col_offset = 2
  caves = set()
  locations = []
  artifacts = []
  sitings = []

  for i in xrange(15):
    name = sheet.cell(0, col_offset + i).value
    locations.append({
      'id': i,
      'name': name,
      'col_idx': col_offset + i
    })

  row_offset = 3
  for i in xrange(176):
    artifact_name = sheet.cell(row_offset + i, 0)
    artifact_chinese_name = sheet.cell(row_offset + i, 1)
    artifacts.append({
      'id': i,
      'name': artifact_name.value,
      'chinese_name': artifact_chinese_name.value,
      'row_idx': row_offset + i
    })

  for artifact in artifacts:
    for location in locations:
      cell = sheet.cell(artifact['row_idx'], location['col_idx'])
      cave_numbers = cave_numbers_for_cell(cell)
      for cave in cave_numbers:
        caves.add(cave)
        
  print caves

filename = sys.argv[1]
print "Opening", filename
read_file(filename)
      