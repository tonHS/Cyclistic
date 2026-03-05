#!/usr/bin/env python3
"""Generate a professional PDF design document for the Cyclistic case study."""

from fpdf import FPDF

class DesignDocPDF(FPDF):
    BLUE = (41, 98, 155)
    DARK = (44, 62, 80)
    GRAY = (100, 100, 100)
    LIGHT_BG = (245, 247, 250)
    WHITE = (255, 255, 255)
    ACCENT = (230, 126, 34)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*self.GRAY)
            self.cell(0, 8, "Cyclistic Bike-Share Case Study | Analysis Design Document", align="R")
            self.ln(4)
            self.set_draw_color(*self.BLUE)
            self.set_line_width(0.4)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*self.GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*self.BLUE)
        self.cell(0, 10, title)
        self.ln(8)
        self.set_draw_color(*self.BLUE)
        self.set_line_width(0.6)
        self.line(self.l_margin, self.get_y(), self.l_margin + 50, self.get_y())
        self.ln(6)

    def sub_title(self, title):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.DARK)
        self.cell(0, 8, title)
        self.ln(7)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=10):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        x = self.get_x()
        self.set_x(x + indent)
        # bullet character
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.ACCENT)
        self.cell(5, 5.5, "-")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bold_bullet(self, bold_part, rest, indent=10):
        self.set_x(self.get_x() + indent)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.ACCENT)
        self.cell(5, 5.5, "- ")
        self.set_text_color(*self.DARK)
        self.cell(self.get_string_width(bold_part) + 1, 5.5, bold_part)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, rest)
        self.ln(1)

    def table_row(self, cells, widths, bold=False, fill=False):
        h = 7
        style = "B" if bold else ""
        if fill:
            self.set_fill_color(*self.LIGHT_BG)
        self.set_font("Helvetica", style, 9)
        self.set_text_color(*self.DARK)
        for i, (cell, w) in enumerate(zip(cells, widths)):
            self.cell(w, h, cell, border=0, fill=fill)
        self.ln(h)


def build_pdf(output_path):
    pdf = DesignDocPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)

    # ── TITLE PAGE ──
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*DesignDocPDF.BLUE)
    pdf.cell(0, 14, "Cyclistic Bike-Share", align="C")
    pdf.ln(16)
    pdf.set_font("Helvetica", "", 20)
    pdf.set_text_color(*DesignDocPDF.DARK)
    pdf.cell(0, 12, "Analysis Design Document", align="C")
    pdf.ln(20)

    # Decorative line
    cx = pdf.w / 2
    pdf.set_draw_color(*DesignDocPDF.ACCENT)
    pdf.set_line_width(1.2)
    pdf.line(cx - 40, pdf.get_y(), cx + 40, pdf.get_y())
    pdf.ln(20)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(*DesignDocPDF.GRAY)
    pdf.cell(0, 8, "Prepared for: Lily Moreno, Director of Marketing", align="C")
    pdf.ln(8)
    pdf.cell(0, 8, "Prepared by: Marketing Analytics Team", align="C")
    pdf.ln(8)
    pdf.cell(0, 8, "Date: March 2026", align="C")
    pdf.ln(8)
    pdf.cell(0, 8, "Data Period: January - December 2025", align="C")

    # ── SECTION 1: BUSINESS TASK ──
    pdf.add_page()
    pdf.section_title("1. Business Task")

    pdf.sub_title("Primary Question")
    pdf.body_text("How do annual members and casual riders use Cyclistic bikes differently?")

    pdf.sub_title("Business Objective")
    pdf.body_text(
        "Identify behavioral differences between casual riders and annual members "
        "to inform a marketing strategy aimed at converting casual riders into annual members."
    )

    pdf.sub_title("Context")
    pdf.body_text(
        "Cyclistic's finance analysts have concluded that annual members are much more profitable "
        "than casual riders. Rather than targeting all-new customers, the Director of Marketing "
        "believes there is a strong opportunity to convert existing casual riders into members, "
        "since they are already aware of the Cyclistic program. This analysis provides the "
        "data-driven foundation for that conversion strategy."
    )

    pdf.sub_title("Key Stakeholders")
    pdf.bullet("Lily Moreno - Director of Marketing (project sponsor)")
    pdf.bullet("Cyclistic Marketing Analytics Team (analysis & execution)")
    pdf.bullet("Cyclistic Executive Team (approval authority)")

    # ── SECTION 2: DATA SOURCE ──
    pdf.section_title("2. Data Source")

    pdf.body_text(
        "Source: Divvy/Motivate International Inc. public trip data, used as a proxy for "
        "the fictional Cyclistic company. Made available under public license; no personally "
        "identifiable information (PII) is included."
    )

    pdf.sub_title("Dataset Overview")
    pdf.bullet("Period: January 2025 through December 2025 (full calendar year)")
    pdf.bullet("Volume: ~5.55 million individual ride records")
    pdf.bullet("Format: 12 monthly CSV files, 13 columns each")
    pdf.bullet("January file: Updated version (202501-divvy-tripdata-2_2026Feb4.csv, ~138,690 rows)")

    pdf.sub_title("Schema (13 Columns)")

    cols = [
        ("ride_id", "string", "Unique trip identifier"),
        ("rideable_type", "string", "classic_bike or electric_bike"),
        ("started_at", "datetime", "Trip start timestamp"),
        ("ended_at", "datetime", "Trip end timestamp"),
        ("start_station_name", "string", "Starting dock station name (nullable)"),
        ("start_station_id", "string", "Starting dock station ID (nullable)"),
        ("end_station_name", "string", "Ending dock station name (nullable)"),
        ("end_station_id", "string", "Ending dock station ID (nullable)"),
        ("start_lat", "float", "Starting latitude"),
        ("start_lng", "float", "Starting longitude"),
        ("end_lat", "float", "Ending latitude (nullable)"),
        ("end_lng", "float", "Ending longitude (nullable)"),
        ("member_casual", "string", "member or casual"),
    ]
    widths = [45, 20, 105]
    pdf.table_row(["Column", "Type", "Description"], widths, bold=True, fill=True)
    for i, (c, t, d) in enumerate(cols):
        pdf.table_row([c, t, d], widths, fill=(i % 2 == 1))

    pdf.ln(4)
    pdf.sub_title("Known Data Quality Issues")
    pdf.bullet("Missing station names: ~15-22% of rows (predominantly electric bike rides parked outside docks)")
    pdf.bullet("Missing end coordinates: <0.2% of rows lack end_lat/end_lng")
    pdf.bullet("Potential negative ride durations: some rows may have ended_at before started_at")
    pdf.bullet("Extreme ride durations: some rides last days (lost/stolen bikes)")
    pdf.bullet("Possible duplicate ride_ids: will check and deduplicate")

    # ── SECTION 3: DATA CLEANING ──
    pdf.add_page()
    pdf.section_title("3. Data Cleaning & Preparation")

    pdf.sub_title("Tool Choice")
    pdf.body_text(
        "Python (pandas, matplotlib, seaborn) - well-suited for a dataset of ~5.5M rows, "
        "provides reproducible cleaning workflows and publication-quality visualizations."
    )

    pdf.sub_title("Cleaning Steps")
    steps = [
        "Load & combine all 12 monthly CSV files into a single DataFrame.",
        "Deduplicate on ride_id.",
        "Parse started_at and ended_at as datetime objects.",
        "Compute derived columns: ride_length (minutes), day_of_week (name), month (name), hour (0-23), season (Winter/Spring/Summer/Fall).",
        "Remove rides with ride_length <= 0 (timestamp errors).",
        "Remove rides with ride_length < 1 minute (false starts / redocks).",
        "Remove rides with ride_length > 24 hours (lost/stolen bikes, not representative).",
        "Document row counts before and after each cleaning step for full transparency.",
    ]
    for i, step in enumerate(steps, 1):
        pdf.bullet(f"Step {i}: {step}")

    # ── SECTION 4: ANALYSIS PLAN ──
    pdf.section_title("4. Analysis Plan")

    pdf.sub_title("Dimension 1: Ride Volume & Composition")
    pdf.bullet("Total rides by member type (overall proportion split)")
    pdf.bullet("Rides by member type per month (seasonality patterns)")
    pdf.bullet("Rides by member type per day of week (weekday vs. weekend behavior)")
    pdf.bullet("Rides by member type per hour of day (commute vs. leisure timing)")

    pdf.sub_title("Dimension 2: Ride Duration")
    pdf.bullet("Mean and median ride duration by member type")
    pdf.bullet("Ride duration distribution comparison (casual vs. member)")
    pdf.bullet("Mean ride duration by member type x day of week")
    pdf.bullet("Mean ride duration by member type x month")

    pdf.sub_title("Dimension 3: Bike Type Preference")
    pdf.bullet("Classic vs. electric bike split by member type")
    pdf.bullet("Bike type usage trends across time dimensions")

    pdf.sub_title("Dimension 4: Geographic Patterns")
    pdf.bullet("Top 10 start stations for casual riders vs. members")
    pdf.bullet("Top 10 end stations for casual riders vs. members")
    pdf.bullet("Round-trip vs. one-way ride analysis (same start/end station)")
    pdf.bullet("Note: Station analysis covers the ~78-85% of rides with station data")

    pdf.sub_title("Dimension 5: Seasonal & Weather-Driven Patterns")
    pdf.bullet("Month-over-month ride volume trends by member type")
    pdf.bullet("Seasonal ride duration patterns")
    pdf.bullet("How the casual/member ratio shifts across seasons")

    # ── SECTION 5: PLANNED VISUALIZATIONS ──
    pdf.add_page()
    pdf.section_title("5. Planned Executive Deck Visualizations")

    slides = [
        ("Title Slide", "--", "Cyclistic branding, business task, date"),
        ("Executive Summary", "Bullet points", "Key findings and 3 recommendations upfront"),
        ("Ride Volume Split", "Donut chart", "Overall member vs. casual proportion"),
        ("Monthly Trends", "Dual-line chart", "Seasonality: member vs. casual ride counts"),
        ("Day-of-Week", "Grouped bar chart", "Weekday vs. weekend behavior contrast"),
        ("Hourly Usage", "Dual-line chart", "Commute peaks (members) vs. leisure spread"),
        ("Ride Duration", "Bar chart", "Average duration differences by rider type"),
        ("Duration x Day", "Grouped bar chart", "Duration by day of week by rider type"),
        ("Bike Type Pref.", "Grouped bar chart", "Classic vs. electric preference by type"),
        ("Top Stations (Casual)", "Horizontal bar", "Where casual riders concentrate"),
        ("Top Stations (Member)", "Horizontal bar", "Where members ride most"),
        ("Seasonal Ratio", "Stacked area/line", "How casual share grows in summer"),
        ("Recommendations", "Bullet points", "3 data-backed marketing recommendations"),
    ]
    widths_s = [40, 35, 95]
    pdf.table_row(["Slide", "Chart Type", "Purpose"], widths_s, bold=True, fill=True)
    for i, (s, c, p) in enumerate(slides):
        pdf.table_row([s, c, p], widths_s, fill=(i % 2 == 1))

    pdf.ln(6)
    pdf.sub_title("Visual Design Standards")
    pdf.bullet("Consistent two-color palette: dark blue (members) and coral/orange (casual riders)")
    pdf.bullet("Clean white backgrounds with minimal gridlines")
    pdf.bullet("Clear titles, axis labels, and data callouts on every chart")
    pdf.bullet("Insight-driven chart titles (e.g., 'Casual riders take 2x longer rides')")
    pdf.bullet("Executive-friendly: no jargon, one key insight per slide")

    # ── SECTION 6: DELIVERABLE ──
    pdf.section_title("6. Deliverable")

    pdf.body_text(
        "Format: Self-contained HTML presentation file with embedded charts, viewable "
        "in any browser with no external dependencies."
    )
    pdf.ln(2)
    pdf.sub_title("Structure")
    pdf.bullet("~13 slides with progressive narrative flow")
    pdf.bullet("Each slide contains one key insight paired with one visualization")
    pdf.bullet("Opens with executive summary, closes with actionable recommendations")
    pdf.bullet("All charts embedded as inline base64 images (fully portable, no files needed)")

    # ── SECTION 7: ASSUMPTIONS & LIMITATIONS ──
    pdf.section_title("7. Assumptions & Limitations")

    limitations = [
        ("No PII: ", "Cannot determine if casual riders are tourists vs. local residents, or link multiple trips to the same individual."),
        ("No pricing data: ", "Cannot calculate revenue impact, lifetime value, or price sensitivity."),
        ("Station gaps: ", "~15-22% of rides lack station names; station-level analysis represents the docked-ride subset only."),
        ("Single year: ", "Analysis covers 2025 only; year-over-year growth trends are not possible."),
        ("No weather data: ", "Seasonal patterns are observed but cannot be directly attributed to specific weather conditions."),
        ("Inferred ride purpose: ", "Commute vs. leisure usage is inferred from temporal patterns (e.g., weekday rush hour = commute), not from explicit rider-reported data."),
    ]
    for bold_part, rest in limitations:
        pdf.bold_bullet(bold_part, rest)

    # ── APPROVAL ──
    pdf.ln(8)
    pdf.set_draw_color(*DesignDocPDF.ACCENT)
    pdf.set_line_width(0.8)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*DesignDocPDF.BLUE)
    pdf.cell(0, 10, "Awaiting Approval", align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*DesignDocPDF.DARK)
    pdf.multi_cell(0, 5.5,
        "Please review this design document. Once approved, the team will proceed with "
        "data cleaning, analysis, and executive deck production.",
        align="C"
    )

    pdf.output(output_path)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    output = "/Users/admin/Desktop/Misc Fall 2024/Google course/Cyclistic Case Study using AI_2026/Cyclistic_Analysis_Design_Document.pdf"
    build_pdf(output)
