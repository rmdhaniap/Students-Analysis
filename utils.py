def group_by(data, column: str):
    """
    Mengelompokkan data berdasarkan kolom tertentu, 
    lalu menghitung jumlah target untuk setiap label (Graduate, Dropout, Enrolled).
    """
    distribution = data.groupby(column).agg(
        Target_graduated=("Target", lambda x: (x == "Graduate").sum()),
        Target_dropout=("Target", lambda x: (x == "Dropout").sum()),
        Target_enrolled=("Target", lambda x: (x == "Enrolled").sum()),
    ).reset_index()

    return distribution


def melt(df_group_by, column: str):
    """
    Mengubah dataframe hasil group_by menjadi format long (melted),
    agar dapat digunakan untuk visualisasi (misal: barplot dengan hue).
    """
    df_distribution = df_group_by.melt(
        id_vars=[column],
        value_vars=[
            "Target_graduated", 
            "Target_dropout", 
            "Target_enrolled"
        ],
        var_name="Target",
        value_name="Count"
    )
    return df_distribution

def avg_value(value1, value2):
    return (value1 + value2) / 2

def get_key(data, val):
    return [key for key, value in data.items() if value == val][0]
