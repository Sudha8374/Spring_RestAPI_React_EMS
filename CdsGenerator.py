from staging import VerticaRequests
import pandas as pd
from pip._vendor.distlib.compat import raw_input

v = VerticaRequests()



# Hard coded values for testing
# schemaName = 'UNIVERSALHS_MILLENNIUM  '
# tableValue = 'PFT_LINE_ITEM'
# aliasValue = 'PLI'
# cdsTableName = 'MD_F_LINE_ITEM'

print("************* CDS SQL STATEMENT GENERATOR ************************")
schemaName = raw_input("SCHEMA NAME (if schema is UNIVERSALHS_MILLENNIUM    just click enter):")
if len(schemaName) == 0:
    schemaName = 'UNIVERSALHS_MILLENNIUM   '

tableValue = raw_input("TABLE NAME:")

x = tableValue.split('_')
len1 = x.__len__()
alias = ""
for i in range(0, len1):
    alias += x[i][0]
aliasValue = alias.upper()


cdsTableName = raw_input("CDS NAME:")


print("GENERATING SQL STATEMENT \r\n")


print("**************** START COPYING QUERY FROM HERE. **************** \r\n")
query = "SELECT \r\n"
codevaluequery = "SELECT \r\n"


# To generate the sql statements for the code fields
def convert_to_code_field(code_value, alias):
    x = code_value.split('_')
    len = x.__len__() - 1
    code_value = ""
    for i in range(len - 1, -1, -1):
        code_value = x[i] + '_' + code_value
    raw_code = code_value + "RAW_CODE"
    raw_display = code_value + "RAW_DISPLAY"
    raw_cdf = code_value + "RAW_CDF"

    codevaluesql = alias + "." + code_value + "CD::INT AS " + raw_code + ",\r\n"
    codevaluesql += "NULL::VARCHAR(80) AS " + raw_display + ",\r\n"
    codevaluesql += "NULL::VARCHAR(24) AS " + raw_cdf + ","
    global codevaluequery
    codevaluequery += "        " + code_value[:-1] + "." + "DISPLAY AS " + raw_display + ",\r\n"
    codevaluequery += "        " + code_value[:-1] + "." + "CDF_MEANING AS " + raw_cdf + ",\r\n"
    return codevaluesql

# To generate the sql statements for the date fields
def convert_to_date_field(self, alias):
    if "UPDT" in self:
        return alias + "." + self + "::TIMESTAMPTZ AS UPDATE_RAW_DT_TM,"
    else:
        x = self.split('_')
        len = x.__len__()
        temp = ""
        for i in range(len - 3, -1, -1):
            temp = x[i] + '_' + temp
        raw_date = temp + "RAW_DT_TM"
        return alias + "." + self + "::TIMESTAMPTZ AS " + raw_date + ","


# To expant and generate the sql statements for the fields
def convert_to_expanded_field(self, alias):
    # Change this to contains
    if "UPDT_CNT" in self:
        column = self.replace("UPDT_CNT", "UPDATE_COUNT")
        return alias + "." + self + "::INT AS " + column + ","
    elif "UPDT" in self:
        column = self.replace("UPDT", "UPDATE")
        return alias + "." + self + "::INT AS " + column + ","
    elif "NBR" in self:
        column = self.replace("NBR", "NUMBER")
        return alias + "." + self + "::INT AS " + column + ","


# To generate the sql statements for the fields
def convert_other_fields(tableColumn, table, dataType, alias):
    return alias + "." + tableColumn + "::" + dataType + " AS " + tableColumn + ","

# To generate the sql statements for the personal fields
def convert_personal_fields(tableColumn, alias):
    personal = alias + "." + tableColumn + "::INT AS " + tableColumn + ",\r\n"
    personal += tableColumn[:-3] + ".NAME_FULL_FORMATTED::VARCHAR(200) AS " + tableColumn[:-3] + "_NAME,"
    return personal

# To exclude the unwanted fields from the sql statement
def exclude_unwanted_fields(tableColumn):
    return ""


# To check for the different fields based on the type and the name of the fields
def check_for_field_type(column, table, dataType, alias):
    var1 = column
    x = var1.split('_')
    len = x.__len__() - 1

    if "ACTIVE_STATUS_CD" in column or "ACTIVE_STATUS_PRSNL_ID" in column or "LAST_UTC_TS" in column or "UPDT_APPLCTX" in column or "INST_ID" in column or "TXN_ID_TEXT" in column or "UPDT_TASK" in column:
        return exclude_unwanted_fields(column)
    elif x[len] == "CD":
        return convert_to_code_field(column, alias)
    elif x[len] == "TM":
        return convert_to_date_field(column, alias)
    elif "UPDT" in column or "NBR" in column:
        return convert_to_expanded_field(column, alias)
    elif "PRSNL_ID" in column:
        return convert_personal_fields(column, alias)
    else:
        return convert_other_fields(column, table, dataType, alias)

query1 = "select table_name, COLUMN_NAME, DATA_TYPE from v_catalog.columns where table_name ='"+tableValue.upper()+"' and table_schema ='"+schemaName.upper()+"' order by column_name"

cur = v.vertica_get(query1, 'N', None, None)

df = pd.DataFrame(cur, columns=['table_name', 'COLUMN_NAME', 'DATA_TYPE'])

code_dict = dict()
personalFieldList = []
alias = aliasValue.upper()
for ind in df.index:
    table = df['table_name'][ind].upper()
    tableColumn = df['COLUMN_NAME'][ind].upper()
    datatype = df['DATA_TYPE'][ind].upper()
    if "CD" in tableColumn:
        x = tableColumn.split('_')
        len = x.__len__() - 1
        code_value = ""
        for i in range(len - 1, -1, -1):
            code_value = x[i] + '_' + code_value
        code_dict[tableColumn] = code_value[:-1]
    if "PRSNL_ID" in tableColumn and "ACTIVE_STATUS_PRSNL_ID" not in tableColumn:
        personalFieldList.append(tableColumn)
    line = check_for_field_type(tableColumn, table, datatype, alias)
    if line != "":
        query += line + "\r\n"


query = query[:-3]

#To generate the md time and generate end of the statement

query += ",\r\nSYSDATE::TIMESTAMPTZ AS MD_UPDATE_DT_TM\r\nFROM "+schemaName+"." + table + " " + alias +"\r\n"

for p in personalFieldList:
    query += "LEFT JOIN ~~millenniumSchemaName~~.PRSNL "+p[:-3] +" ON "+alias+"."+p+" = "+p[:-3]+".PERSON_ID \r\n"

codevaluequery = codevaluequery[:-3]
codevaluequery += "\r\nFROM ~~cdsSchemaName~~." + cdsTableName + " " + alias +"\r\n"
for key, value in code_dict.items():
    codevaluequery +="LEFT JOIN "+schemaName+".CODE_VALUE "+value+" ON "+value+".CODE_VALUE = "+alias+"."+key+"\r\n"
print(query)
print("\r\n")


print(codevaluequery)
print("**************** QUERY ENDS HERE ****************\r\n")
