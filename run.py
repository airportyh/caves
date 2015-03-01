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
      for i in xrange(start_range, end_range):
        numbers.append(unicode(i))
    else:
      numbers.append(unicode(part))
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
    assert has_all_unicodes(numbers)
    return numbers
  else:
    return []

def has_all_unicodes(lst):
  if type(lst) != list:
    return False
  for n in lst:
    if type(n) != unicode:
      return False
  return True

if len(sys.argv) < 2:
  print "Usage: python run.py <excel file>"
  sys.exit()

def read_architectures(sheet, ncols):
  archs = []
  col_offset = 2
  for idx in xrange(col_offset, ncols):
    name = sheet.cell(0, idx).value
    archs.append({
      'name': name,
      'col_idx': idx
    })
  return archs

def is_icon_type_header(cell, xf_list):
  return xf_list[cell.xf_index].border.bottom_line_style == 6

def read_icons(sheet, nrows, xf_list):
  icons = []
  icon_types = []
  row_offset = 3
  current_icon_type = None
  for idx in xrange(row_offset, nrows):
    cell = sheet.cell(idx, 0)
    if is_icon_type_header(cell, xf_list):
      current_icon_type = {
        'name': cell.value.strip(),
        'chinese_name': sheet.cell(idx, 1).value.strip()
      }
      icon_types.append(current_icon_type)
    else:
      icon_name = cell.value
      icon_chinese_name = sheet.cell(idx, 1).value
      icons.append({
        'name': icon_name,
        'chinese_name': icon_chinese_name,
        'icon_type': current_icon_type,
        'row_idx': idx
      })
  return icons, icon_types

def read_file(filename):
  # open first time just to get ncols and nrows wo formatting info
  book = xlrd.open_workbook(filename)
  sheet = book.sheet_by_index(0)
  ncols = sheet.ncols
  nrows = sheet.nrows

  # reopen to get format info
  book = xlrd.open_workbook(filename, formatting_info=True)
  sheet = book.sheet_by_index(0)
  
  caves = set()
  sitings = []

  architectures = read_architectures(sheet, ncols)
  print 'num architectures:', len(architectures)

  icons, icon_types = read_icons(sheet, nrows, book.xf_list)
  print 'num icons:', icons
  print 'icon types:', icon_types

  for artifact in icons:
    for arch in architectures:
      cell = sheet.cell(artifact['row_idx'], arch['col_idx'])
      cave_numbers = cave_numbers_for_cell(cell)
      for cave in cave_numbers:
        caves.add(cave)
        
  print 'num caves:', len(caves)
  print caves

filename = sys.argv[1]
print "Opening", filename
read_file(filename)
      