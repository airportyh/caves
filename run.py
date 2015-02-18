import xlrd

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
        numbers = str(cell.value)
      else:
        try:
          numbers = cell.value.replace('\xef\xbc\x8c', ',')
        except UnicodeDecodeError, e:
          print "Cant replace", cell.value
          print repr(cell.value)
          raise e
      print "These caves have a", artifact['name'], "in in the", location['name'], ":", numbers
      
      