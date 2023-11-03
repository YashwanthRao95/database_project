# This file is used to generate ouput as per reqiurements
def pd2sql(dtype):
    """Function to convert pandas dtype to SQL data type."""
    if "int" in str(dtype):
        return "INT"
    elif "float" in str(dtype):
        return "FLOAT"
    elif "object" in str(dtype):
        return "VARCHAR(255)"
    elif "datetime" in str(dtype):
        return "DATETIME"
    else:
        return "TEXT"


def output_1NF(primary_keys, df):
    primary_key = list(df.keys())[0]
    table_name = "_".join(primary_key) + "_table"
    df = df[primary_key]
    query = f"CREATE TABLE {table_name} (\n"

    for column, dtype in zip(df.columns, df.dtypes):
        if column in primary_keys:
            query += f"  {column} {pd2sql(dtype)} PRIMARY KEY,\n"
        else:
            query += f"  {column} {pd2sql(dtype)},\n"

    query = query.rstrip(',\n') + "\n);"

    print(query)


def output_2_3(relations):
    for relation_name, relation in relations.items():
        primary_keys = relation_name
        primary_keys = (primary_keys,) if isinstance(
            primary_keys, str) else primary_keys
        table_name = "_".join(primary_keys) + '_table'

        if table_name.count('_') >= 2:
            query = f"CREATE TABLE {table_name} (\n"

            for column, dtype in zip(relation.columns, relation.dtypes):
                if column in primary_keys:
                    query += f" FOREIGN KEY ({column}) REFERENCES {column.replace('_fk','')}_table({column.replace('_fk','')}),\n"
                else:
                    query += f"  {column} {pd2sql(dtype)},\n"

            query = query.rstrip(',\n') + "\n);"
        else:
            query = f"CREATE TABLE {table_name} (\n"

            for column, dtype in zip(relation.columns, relation.dtypes):
                if column in primary_keys:
                    query += f"  {column} {pd2sql(dtype)} PRIMARY KEY,\n"
                else:
                    query += f"  {column} {pd2sql(dtype)},\n"

            query = query.rstrip(',\n') + "\n);"

        print(query)


def output_BCNF_4_5(relations):
    for relation_name, relation in relations.items():
        primary_keys = relation_name
        primary_keys = (primary_keys,) if isinstance(
            primary_keys, str) else primary_keys
        table_name = "_".join(primary_keys) + '_table'

        query = f"CREATE TABLE {table_name} (\n"

        for column, dtype in zip(relation.columns, relation.dtypes):
            if column == primary_keys:
                query += f"  {column} {pd2sql(dtype)} PRIMARY KEY,\n"
            elif '_fk' in column:
                query += f" FOREIGN KEY ({column}),\n"
            else:
                query += f"  {column} {pd2sql(dtype)},\n"

        query = query.rstrip(',\n') + "\n);"

        print(query)
