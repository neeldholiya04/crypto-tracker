import pandas as pd
from googleapiclient.errors import HttpError
from gspread_formatting import (
    CellFormat, Color, TextFormat, format_cell_range
)


def format_data_frame(data_frame):
    """
    Format the given DataFrame:
    - Capitalizes the 'Symbol' column
    - Formats currency and percentage fields
    """
    try:
        currency_columns = ["Current Price (USD)", "Market Cap (USD)", "Total Volume (USD)"]
        for col in currency_columns:
            if col in data_frame.columns:
                data_frame[col] = pd.to_numeric(data_frame[col], errors="coerce")
                data_frame[col] = data_frame[col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")

        percentage_columns = ["24h Price Change (%)"]
        for col in percentage_columns:
            if col in data_frame.columns:
                data_frame[col] = pd.to_numeric(data_frame[col], errors="coerce")
                data_frame[col] = data_frame[col].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A")

        if "Symbol" in data_frame.columns:
            data_frame["Symbol"] = data_frame["Symbol"].str.upper()

        return data_frame
    except Exception as e:
        print(f"Error formatting DataFrame: {e}")
        return data_frame
def beautify_sheet(sheet, service, sheet_id):
    """
    Apply professional formatting to the Google Sheet.
    Includes column width adjustment, bold headers, alignment, freezing the header row, and adding borders.
    """
    try:
        requests = [
            # Column Width Requests
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 1
                    },
                    "properties": {
                        "pixelSize": 250
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 1,
                        "endIndex": 2
                    },
                    "properties": {
                        "pixelSize": 120
                    },
                    "fields": "pixelSize"
                }
            },
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 2,
                        "endIndex": 6
                    },
                    "properties": {
                        "pixelSize": 200
                    },
                    "fields": "pixelSize"
                }
            },
            # Center Alignment for All Columns
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endColumnIndex": 6
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER"
                        }
                    },
                    "fields": "userEnteredFormat.horizontalAlignment"
                }
            },
            # Freeze Header Row
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "gridProperties": {
                            "frozenRowCount": 1
                        }
                    },
                    "fields": "gridProperties.frozenRowCount"
                }
            },
            # Bold Header Row
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {
                                "bold": True
                            }
                        }
                    },
                    "fields": "userEnteredFormat.textFormat.bold"
                }
            },
            # Add Borders to All Cells
            {
                "updateBorders": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endRowIndex": sheet.row_count,
                        "endColumnIndex": sheet.col_count
                    },
                    "top": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0, "green": 0, "blue": 0}
                    },
                    "bottom": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0, "green": 0, "blue": 0}
                    },
                    "left": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0, "green": 0, "blue": 0}
                    },
                    "right": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0, "green": 0, "blue": 0}
                    },
                    "innerHorizontal": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0, "green": 0, "blue": 0}
                    },
                    "innerVertical": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0, "green": 0, "blue": 0}
                    }
                }
            }
        ]

        # Execute the batch update request
        service.spreadsheets().batchUpdate(
            spreadsheetId=sheet.spreadsheet.id,
            body={"requests": requests}
        ).execute()

        # Apply header cell styling using gspread-formatting
        header_range = f"A1:{chr(65 + sheet.col_count - 1)}1"
        format_cell_range(sheet, header_range, CellFormat(
            backgroundColor=Color(0.129, 0.588, 0.953),
            textFormat=TextFormat(
                bold=True,
                foregroundColor=Color(1, 1, 1)
            ),
            horizontalAlignment="CENTER"
        ))

        print("Professional sheet styling applied successfully.")
    except HttpError as e:
        print(f"HTTP Error beautifying the Google Sheet: {e}")
    except Exception as e:
        print(f"Error beautifying the Google Sheet: {e}")