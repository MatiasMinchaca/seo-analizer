import pandas as pd
from openpyxl.styles import PatternFill, Font
from config import ISSUE_DETAILS, HEADER_COLOR

def generate_xlsx_report(issues, base_url, crawled_count):
    """Analyzes the data and generates a styled report in XLSX format."""
    report_filename = "seo_audit_report.xlsx"
    with pd.ExcelWriter(report_filename, engine='openpyxl') as writer:
        # --- Styles ---
        header_fill = PatternFill(start_color=HEADER_COLOR, end_color=HEADER_COLOR, fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True)

        # --- Summary Sheet ---
        summary_list = [("Metric", "Value"), ("Base URL", base_url), ("Pages Crawled", crawled_count), ("", "")]
        for issue_key, details in ISSUE_DETAILS.items():
            if issues.get(issue_key):
                summary_list.append((details["sheet_name"], len(issues[issue_key])))
        
        summary_df = pd.DataFrame(summary_list[1:], columns=summary_list[0])
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        ws = writer.sheets["Summary"]
        for cell in ws["A"] + ws[1]:
            cell.fill = header_fill
            cell.font = header_font

        # --- Issue Sheets ---
        for issue_key, details in ISSUE_DETAILS.items():
            data = issues.get(issue_key)
            if not data: continue

            sheet_name = details["sheet_name"]
            info_df = pd.DataFrame([{"Info": details["description"]}, {"Info": details["recommendation"]}])
            info_df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=0)

            # Create DataFrame from issue data
            issue_df = pd.DataFrame(data)
            
            if not issue_df.empty:
                issue_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=3)
                ws = writer.sheets[sheet_name]
                # Style headers
                for cell in ws[1] + ws[2]: # Description and Recommendation
                    cell.fill = header_fill
                    cell.font = header_font
                for cell in ws[4]: # Data headers
                    cell.fill = header_fill
                    cell.font = header_font

        # --- Auto-adjust column widths for all sheets ---
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column_cells in worksheet.columns:
                max_length = 0
                for cell in column_cells:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column_cells[0].column_letter].width = adjusted_width

    print(f"\nSEO analysis XLSX report saved to {report_filename}")
