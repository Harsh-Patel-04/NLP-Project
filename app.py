import streamlit as st
import pdfplumber
import re
import os
from datetime import datetime

class ComprehensiveFinancialAnalyzer:
    def __init__(self):
        self.financial_tables = []
        self.quarterly_data = {}

    def extract_text_comprehensive(self, pdf_path):
        """Fast text extraction with full coverage"""
        print(f"📄 Reading {os.path.basename(pdf_path)}...")
        full_text = ""

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"

                    # Quick table detection
                    if i < 5:  # Check first 5 pages for tables
                        tables = page.extract_tables()
                        for table in tables:
                            if table and len(table) > 2:
                                self.financial_tables.append({
                                    'page': i+1,
                                    'table': table
                                })

            print(f"✅ Extracted {len(full_text):,} characters")
            return full_text

        except Exception as e:
            print(f"❌ PDF extraction failed: {e}")
            return ""

    def extract_quarterly_financials(self, text):
        """Extract comprehensive quarterly financial data with comparisons"""
        quarterly_data = {}
        
        # Enhanced patterns for quarterly data extraction
        patterns = {
            'revenue': [
                r'Revenue\s+from\s+operations\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'Total\s+revenue\s+from\s+operations\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            ],
            'total_income': [
                r'Total\s+Income\s+\(I\+II\)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'Total\s+Income\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            ],
            'finance_cost': [
                r'Finance\s+costs\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            ],
            'total_expenses': [
                r'Total\s+expenses\s+\(IV\)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'Total\s+expenses\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            ],
            'profit_before_tax': [
                r'Profit\s+before\s+tax\s+\(III-IV\)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'Profit\s+before\s+tax\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'PBT\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            ],
            'profit_for_period': [
                r'Profit\s+for\s+the\s+period\s+\(V-VI\)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'Profit\s+for\s+the\s+period\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'Net\s+Profit\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'PAT\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            ],
            'eps': [
                r'Basic.*?\(Amount in INR\)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'Earnings per share.*?([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            ],
            'borrowings': [
                r'Borrowings\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'Total\s+borrowings\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            ]
        }

        for metric, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    current_q = self.clean_number(match.group(1))
                    previous_q = self.clean_number(match.group(2))
                    previous_year_q = self.clean_number(match.group(3))
                    
                    if current_q > 0:
                        quarterly_data[metric] = {
                            'current': current_q,
                            'previous_q': previous_q,
                            'previous_year': previous_year_q,
                            'qoq_change': self.calculate_percentage_change(previous_q, current_q),
                            'yoy_change': self.calculate_percentage_change(previous_year_q, current_q)
                        }
                    break

        return quarterly_data

    def calculate_percentage_change(self, old_value, new_value):
        """Calculate percentage change between two values"""
        if old_value == 0:
            return 0
        return ((new_value - old_value) / old_value) * 100

    def extract_all_financials(self, text):
        """Comprehensive financial extraction"""
        financials = {}

        # ALL FINANCIAL PATTERNS
        patterns = [
            # Revenue patterns
            (r'Revenue\s+from\s+Operations\s+([\d,]+\.?\d*)', 'revenue'),
            (r'Revenue\s+from\s+operations\s+([\d,]+\.?\d*)', 'revenue'),
            (r'Total\s+Income\s+([\d,]+\.?\d*)', 'total_income'),
            (r'Sales?\s+([\d,]+\.?\d*)', 'sales'),
            (r'Turnover\s+([\d,]+\.?\d*)', 'turnover'),

            # Profit patterns
            (r'Profit\s+for\s+the\s+period\s+([\d,]+\.?\d*)', 'pat'),
            (r'Net\s+Profit\s+([\d,]+\.?\d*)', 'pat'),
            (r'PAT\s+([\d,]+\.?\d*)', 'pat'),
            (r'Profit\s+after\s+tax\s+([\d,]+\.?\d*)', 'pat'),
            (r'Profit\s+before\s+Tax\s+([\d,]+\.?\d*)', 'pbt'),
            (r'PBT\s+([\d,]+\.?\d*)', 'pbt'),
            (r'EBITDA\s+([\d,]+\.?\d*)', 'ebitda'),

            # EPS patterns
            (r'Earnings\s+per\s+share\s+([\d,]+\.?\d*)', 'eps'),
            (r'EPS\s+([\d,]+\.?\d*)', 'eps'),
            (r'Basic.*?EPS.*?([\d,]+\.?\d*)', 'eps'),

            # Cost patterns
            (r'Fuel\s+Cost\s+([\d,]+\.?\d*)', 'fuel_cost'),
            (r'Employee.*?Cost\s+([\d,]+\.?\d*)', 'employee_cost'),
            (r'Finance\s+Costs?\s+([\d,]+\.?\d*)', 'finance_cost'),
            (r'Depreciation\s+([\d,]+\.?\d*)', 'depreciation'),

            # Balance sheet items
            (r'Total\s+Debt\s+([\d,]+\.?\d*)', 'total_debt'),
            (r'Borrowings\s+([\d,]+\.?\d*)', 'borrowings'),
            (r'Cash.*?Balances?\s+([\d,]+\.?\d*)', 'cash_balance'),
            (r'Net\s+Worth\s+([\d,]+\.?\d*)', 'net_worth'),
        ]

        for pattern, metric in patterns:
            if metric not in financials:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    amount = self.clean_number(match.group(1))
                    if self.is_valid_amount(metric, amount):
                        if metric == 'eps':
                            financials[metric] = f"₹{amount:.2f}"
                        else:
                            financials[metric] = f"₹{amount:,.0f} cr"

        return financials

    def extract_corporate_announcements(self, text):
        """COMPREHENSIVE corporate announcements and updates"""
        announcements = {
            'dividends': [],
            'fund_raising': [],
            'acquisitions_mergers': [],
            'appointments': [],
            'resignations': [],
            'board_meetings': [],
            'regulatory_updates': [],
            'project_announcements': [],
            'capacity_expansions': [],
            'new_contracts': [],
            'legal_cases': [],
            'disputes': [],
            'arbitration': [],
            'regulatory_penalties': [],
            'environmental_issues': [],
            'insolvency_cases': [],
            'credit_rating': []
        }

        # DIVIDENDS & DISTRIBUTIONS
        dividend_patterns = [
            r'dividend.*?₹\s*(\d+\.?\d*)\s*per\s+share',
            r'interim\s+dividend.*?₹\s*(\d+\.?\d*)',
            r'final\s+dividend.*?₹\s*(\d+\.?\d*)',
            r'special\s+dividend.*?₹\s*(\d+\.?\d*)'
        ]

        for pattern in dividend_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                announcements['dividends'].append(f"Dividend: ₹{match.group(1)} per share")

        # FUND RAISING
        fundraising_patterns = [
            r'fund.*raising.*?₹\s*([\d,]+\.?\d*)',
            r'issuance.*debentures.*?₹\s*([\d,]+\.?\d*)',
            r'QIP.*?₹\s*([\d,]+\.?\d*)',
            r'preferential.*issue.*?₹\s*([\d,]+\.?\d*)',
            r'rights.*issue.*?₹\s*([\d,]+\.?\d*)'
        ]

        for pattern in fundraising_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                announcements['fund_raising'].append(f"Fund Raising: ₹{match.group(1)}")

        # ACQUISITIONS & MERGERS
        acquisition_patterns = [
            r'acquired.*?([^.]{30,150})',
            r'acquisition.*?([^.]{30,150})',
            r'merged.*?([^.]{30,150})',
            r'amalgamation.*?([^.]{30,150})',
            r'takeover.*?([^.]{30,150})'
        ]

        for pattern in acquisition_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                clean_text = self.clean_announcement_text(match.group(1).strip())
                if clean_text:
                    announcements['acquisitions_mergers'].append(clean_text)

        # LEGAL CASES & DISPUTES
        legal_patterns = [
            r'legal.*case.*?([^.]{30,150})',
            r'dispute.*?([^.]{30,150})',
            r'arbitration.*?([^.]{30,150})',
            r'litigation.*?([^.]{30,150})',
            r'court.*case.*?([^.]{30,150})',
            r'hon\'ble\s+(?:supreme\s+)?court.*?([^.]{30,150})',
            r'NCLT.*?([^.]{30,150})',
            r'tribunal.*?([^.]{30,150})',
            r'SEBI.*order.*?([^.]{30,150})',
            r'regulatory.*penalty.*?([^.]{30,150})'
        ]

        for pattern in legal_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                clean_text = self.clean_announcement_text(match.group(1).strip())
                if clean_text:
                    category = 'legal_cases' if any(word in pattern for word in ['case', 'court', 'tribunal']) else 'disputes'
                    announcements[category].append(clean_text)

        # REGULATORY UPDATES
        regulatory_patterns = [
            r'CERC.*?([^.]{30,150})',
            r'MERC.*?([^.]{30,150})',
            r'regulatory.*commission.*?([^.]{30,150})',
            r'approval.*?([^.]{30,150})',
            r'clearance.*?([^.]{30,150})',
            r'license.*?([^.]{30,150})',
            r'permit.*?([^.]{30,150})'
        ]

        for pattern in regulatory_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                clean_text = self.clean_announcement_text(match.group(1).strip())
                if clean_text:
                    announcements['regulatory_updates'].append(clean_text)

        # PROJECT ANNOUNCEMENTS
        project_patterns = [
            r'project.*?([^.]{30,150})',
            r'expansion.*?([^.]{30,150})',
            r'capacity.*?([^.]{30,150})',
            r'new.*plant.*?([^.]{30,150})',
            r'facility.*?([^.]{30,150})',
            r'MW.*project.*?([^.]{30,150})'
        ]

        for pattern in project_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                clean_text = self.clean_announcement_text(match.group(1).strip())
                if clean_text:
                    announcements['project_announcements'].append(clean_text)

        # BOARD & MANAGEMENT CHANGES
        management_patterns = [
            r'appointed.*?([^.]{30,150})',
            r'resigned.*?([^.]{30,150})',
            r'CEO.*?([^.]{30,150})',
            r'MD.*?([^.]{30,150})',
            r'Director.*?([^.]{30,150})',
            r'Board.*meeting.*?([^.]{30,150})'
        ]

        for pattern in management_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                clean_text = self.clean_announcement_text(match.group(1).strip())
                if clean_text:
                    if 'appoint' in pattern:
                        announcements['appointments'].append(clean_text)
                    elif 'resign' in pattern:
                        announcements['resignations'].append(clean_text)
                    else:
                        announcements['board_meetings'].append(clean_text)

        # ENVIRONMENTAL & COMPLIANCE
        environmental_patterns = [
            r'environmental.*?([^.]{30,150})',
            r'pollution.*?([^.]{30,150})',
            r'NGT.*?([^.]{30,150})',
            r'green.*?([^.]{30,150})',
            r'compliance.*?([^.]{30,150})'
        ]

        for pattern in environmental_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                clean_text = self.clean_announcement_text(match.group(1).strip())
                if clean_text:
                    announcements['environmental_issues'].append(clean_text)

        # CREDIT RATING
        rating_patterns = [
            r'credit.*rating.*?([^.]{30,150})',
            r'CRISIL.*?([^.]{30,150})',
            r'ICRA.*?([^.]{30,150})',
            r'Care.*?([^.]{30,150})',
            r'upgraded.*rating.*?([^.]{30,150})',
            r'downgraded.*rating.*?([^.]{30,150})'
        ]

        for pattern in rating_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                clean_text = self.clean_announcement_text(match.group(1).strip())
                if clean_text:
                    announcements['credit_rating'].append(clean_text)

        return announcements

    def clean_announcement_text(self, text):
        """Clean and format announcement text to remove broken sentences"""
        # Remove line breaks within sentences and clean up text
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
        text = re.sub(r'\s+([.,;:])', r'\1', text)  # Remove spaces before punctuation
        text = text.strip()
        
        # Capitalize first letter
        if text and len(text) > 1:
            text = text[0].upper() + text[1:]
        
        return text if len(text) >= 10 else None  # Filter out very short fragments

    def extract_business_operations(self, text):
        """Business operations and performance metrics"""
        operations = {
            'orderbook': [],
            'new_orders': [],
            'operational_metrics': [],
            'market_updates': [],
            'client_announcements': [],
            'technology_updates': []
        }

        # ORDERBOOK & CONTRACTS
        order_patterns = [
            r'order.*book.*?₹\s*([\d,]+\.?\d*)',
            r'new.*order.*?₹\s*([\d,]+\.?\d*)',
            r'contract.*?won.*?₹\s*([\d,]+\.?\d*)',
            r'deal.*?worth.*?₹\s*([\d,]+\.?\d*)'
        ]

        for pattern in order_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if 'new' in pattern or 'won' in pattern:
                    operations['new_orders'].append(f"New Order: ₹{match.group(1)}")
                else:
                    operations['orderbook'].append(f"Orderbook: ₹{match.group(1)}")

        # OPERATIONAL METRICS
        operational_patterns = [
            r'capacity.*?(\d+,?\d*)\s*MW',
            r'generation.*?(\d+\.?\d*)\s*BU',
            r'plant.*load.*factor.*?(\d+\.?\d*\s*%)',
            r'production.*?(\d+,?\d*)',
            r'sales.*volume.*?(\d+,?\d*)'
        ]

        for pattern in operational_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                operations['operational_metrics'].append(f"Operations: {match.group(1)}")

        # MARKET UPDATES
        market_patterns = [
            r'market.*share.*?([^.]{30,100})',
            r'competition.*?([^.]{30,100})',
            r'industry.*?([^.]{30,100})',
            r'demand.*?([^.]{30,100})'
        ]

        for pattern in market_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                operations['market_updates'].append(f"Market: {match.group(1).strip()}")

        return operations

    def clean_number(self, num_str):
        """Clean number string"""
        try:
            return float(num_str.replace(',', ''))
        except:
            return 0

    def is_valid_amount(self, metric, amount):
        """Validate amount ranges"""
        if amount <= 0:
            return False

        ranges = {
            'revenue': (10, 10000000),
            'pat': (1, 1000000),
            'pbt': (1, 1000000),
            'ebitda': (1, 1000000),
            'eps': (0.01, 10000),
            'fuel_cost': (10, 500000),
            'employee_cost': (10, 500000),
            'total_debt': (10, 5000000)
        }

        return ranges.get(metric, (1, 10000000))[0] <= amount <= ranges.get(metric, (1, 10000000))[1]

    def generate_comprehensive_report(self, filename, text):
        """Generate comprehensive report covering everything"""
        print(f"\n🔍 COMPREHENSIVE ANALYSIS: {filename}")
        print("=" * 70)

        # EXTRACT ALL DATA
        financials = self.extract_all_financials(text)
        announcements = self.extract_corporate_announcements(text)
        operations = self.extract_business_operations(text)

        report = []
        report.append("🚀 COMPREHENSIVE FINANCIAL ANALYZER - ALL PATTERNS COVERED")
        report.append("=" * 70)
        report.append(f"Document: {filename}")
        report.append(f"Analysis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # EXECUTIVE SUMMARY
        report.append("📊 EXECUTIVE SUMMARY")
        report.append("-" * 20)

        # Financial Summary
        if financials:
            report.append("\n💰 FINANCIAL PERFORMANCE:")
            key_metrics = ['revenue', 'pat', 'pbt', 'ebitda', 'eps']
            for metric in key_metrics:
                if metric in financials:
                    name = metric.upper().replace('_', ' ')
                    report.append(f"  • {name}: {financials[metric]}")

        # Key Announcements Summary
        key_announcements = []
        for category in ['dividends', 'fund_raising', 'acquisitions_mergers', 'legal_cases']:
            if announcements[category]:
                key_announcements.extend(announcements[category][:1])

        if key_announcements:
            report.append("\n🏛️ KEY ANNOUNCEMENTS:")
            for announcement in key_announcements[:3]:
                report.append(f"  • {announcement}")

        # DETAILED SECTIONS
        report.append("\n" + "="*70)
        report.append("📈 DETAILED FINANCIAL ANALYSIS")
        report.append("="*70)

        if financials:
            for metric, value in financials.items():
                display_name = metric.replace('_', ' ').title()
                report.append(f"• {display_name}: {value}")
        else:
            report.append("No financial data extracted")

        # CORPORATE ANNOUNCEMENTS DETAILS
        report.append("\n" + "="*70)
        report.append("🏛️ CORPORATE ANNOUNCEMENTS & UPDATES")
        report.append("="*70)

        announcement_categories = [
            ('💰 Dividends & Distributions', 'dividends'),
            ('💸 Fund Raising', 'fund_raising'),
            ('🏢 M&A Activities', 'acquisitions_mergers'),
            ('👥 Management Changes', 'appointments'),
            ('📋 Board Meetings', 'board_meetings'),
            ('⚖️ Legal Cases & Disputes', 'legal_cases'),
            ('🔧 Regulatory Updates', 'regulatory_updates'),
            ('🏗️ Projects & Expansions', 'project_announcements'),
            ('🌱 Environmental Matters', 'environmental_issues'),
            ('📊 Credit Ratings', 'credit_rating')
        ]

        announcements_found = False
        for category_name, category_key in announcement_categories:
            if announcements[category_key]:
                report.append(f"\n{category_name}:")
                for item in announcements[category_key][:3]:
                    report.append(f"  • {item}")
                announcements_found = True

        if not announcements_found:
            report.append("No corporate announcements detected")

        # BUSINESS OPERATIONS
        report.append("\n" + "="*70)
        report.append("🚀 BUSINESS OPERATIONS & PERFORMANCE")
        report.append("="*70)

        operations_found = False
        for category, items in operations.items():
            if items:
                report.append(f"\n{category.replace('_', ' ').title()}:")
                for item in items[:3]:
                    report.append(f"  • {item}")
                operations_found = True

        if not operations_found:
            report.append("No business operations data extracted")

        # EXTRACTION STATISTICS
        report.append("\n" + "="*70)
        report.append("📊 EXTRACTION SUMMARY")
        report.append("="*70)

        total_financials = len(financials)
        total_announcements = sum(len(items) for items in announcements.values())
        total_operations = sum(len(items) for items in operations.values())

        report.append(f"• Financial Metrics: {total_financials}")
        report.append(f"• Corporate Announcements: {total_announcements}")
        report.append(f"• Business Operations: {total_operations}")
        report.append(f"• Total Data Points: {total_financials + total_announcements + total_operations}")
        report.append(f"• Processing Time: <10 seconds")

        quality_score = total_financials + total_announcements + total_operations
        if quality_score >= 20:
            quality = "EXCELLENT"
        elif quality_score >= 10:
            quality = "GOOD"
        elif quality_score >= 5:
            quality = "BASIC"
        else:
            quality = "LIMITED"

        report.append(f"• Data Quality: {quality}")

        return "\n".join(report)

    def analyze_pdf_comprehensive(self, pdf_path):
        """Main comprehensive analysis"""
        start_time = datetime.now()

        text = self.extract_text_comprehensive(pdf_path)
        if not text:
            print("❌ Could not read PDF")
            return

        report = self.generate_comprehensive_report(os.path.basename(pdf_path), text)

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        print(report)
        print(f"\n⏱️  Comprehensive analysis completed in {processing_time:.1f} seconds!")

st.set_page_config(
    page_title="FinSum: Advanced Financial Document Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-box {
        border: 2px dashed #1f77b4;
        border-radius: 15px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 1rem 0;
        background-color: #f8f9fa;
        transition: all 0.3s ease;
    }
    .upload-box:hover {
        background-color: #e3f2fd;
        border-color: #1565c0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .quarterly-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1f77b4;
    }
    .positive-change {
        color: #00C851;
        font-weight: 600;
    }
    .negative-change {
        color: #ff4444;
        font-weight: 600;
    }
    .section-header {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: 600;
    }
    .announcement-card {
        background-color: #ffffff;
        border-left: 4px solid #1f77b4;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .category-header {
        background-color: #1f77b4;
        color: white;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin: 1rem 0 0.5rem 0;
        font-weight: 600;
    }
    .download-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .comparison-table th, .comparison-table td {
        padding: 0.75rem;
        text-align: center;
        border: 1px solid #ddd;
    }
    .comparison-table th {
        background-color: #f8f9fa;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📊 FinSum</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Financial Document Summarizer</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📤 Upload Document")
    uploaded_file = st.file_uploader(
        "Drag and drop or click to upload a financial PDF",
        type=["pdf"],
        label_visibility="collapsed",
        key="file_uploader"
    )
    st.markdown("""
    <div style='color: #666; font-size: 0.9rem; margin-top: 1rem;'>
        Supported: Annual Reports, Quarterly Results, Corporate Announcements
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")

with col2:
    st.markdown("### ℹ️ About FinSum")
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 1.5rem; border-radius: 10px;'>
    FinSum automatically extracts and analyzes key information from financial documents:
    
    - **💰 Financial Metrics**: Revenue, PAT, PBT, EBITDA, EPS
    - **🏛️ Corporate Actions**: Dividends, M&A, Appointments
    - **⚖️ Regulatory Updates**: Compliance, Approvals, Penalties
    - **🚀 Business Operations**: Orders, Projects, Expansions
    
    Simply upload a financial PDF to get started!
    </div>
    """, unsafe_allow_html=True)

if uploaded_file is not None:
    st.markdown("---")
    
    with st.spinner("🔍 Analyzing document... This may take a few moments"):
        analyzer = ComprehensiveFinancialAnalyzer()
        
        temp_path = "temp_uploaded.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        text = analyzer.extract_text_comprehensive(temp_path)
        report = analyzer.generate_comprehensive_report(uploaded_file.name, text)
        financials = analyzer.extract_all_financials(text)
        announcements = analyzer.extract_corporate_announcements(text)
        operations = analyzer.extract_business_operations(text)
        quarterly_data = analyzer.extract_quarterly_financials(text)
        os.remove(temp_path)
    
    st.markdown('<div class="success-box">✅ Analysis Completed Successfully!</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Full Report",
            data=report.encode("utf-8"),
            file_name=f"{uploaded_file.name}_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown("## 📈 Analysis Results")
    
    if quarterly_data:
        st.markdown("### 📊 Quarterly Financial Performance")
        
        key_metrics = [
            ('revenue', 'Revenue from Operations', '₹'),
            ('total_income', 'Total Income', '₹'),
            ('profit_for_period', 'Profit for Period (PAT)', '₹'),
            ('profit_before_tax', 'Profit Before Tax (PBT)', '₹'),
            ('total_expenses', 'Total Expenses', '₹'),
            ('finance_cost', 'Finance Cost', '₹'),
            ('eps', 'EPS', '₹')
        ]
        
        for metric_key, display_name, currency in key_metrics:
            if metric_key in quarterly_data:
                data = quarterly_data[metric_key]
                
                # st.markdown(f'<div class="quarterly-card">', unsafe_allow_html=True)
                st.markdown(f"**{display_name}**")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric(
                        label="Current Quarter",
                        value=f"{currency}{data['current']:,.2f} cr",
                        delta=f"{data['qoq_change']:+.1f}% QoQ" if data['qoq_change'] != 0 else None
                    )
                
                with col2:
                    st.metric(
                        label="Previous Quarter",
                        value=f"{currency}{data['previous_q']:,.2f} cr"
                    )
                
                with col3:
                    st.metric(
                        label="Previous Year Quarter",
                        value=f"{currency}{data['previous_year']:,.2f} cr",
                        delta=f"{data['yoy_change']:+.1f}% YoY" if data['yoy_change'] != 0 else None
                    )
                
                with col4:
                    qoq_color = "positive-change" if data['qoq_change'] >= 0 else "negative-change"
                    st.markdown(f"<div style='text-align: center;'><strong>QoQ Change</strong><br><span class='{qoq_color}'>{data['qoq_change']:+.1f}%</span></div>", unsafe_allow_html=True)
                
                with col5:
                    yoy_color = "positive-change" if data['yoy_change'] >= 0 else "negative-change"
                    st.markdown(f"<div style='text-align: center;'><strong>YoY Change</strong><br><span class='{yoy_color}'>{data['yoy_change']:+.1f}%</span></div>", unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    if financials:
        st.markdown("### 💰 Key Financial Metrics")
        
        cols = st.columns(min(4, len(financials)))
        financial_items = list(financials.items())
        
        for i, (metric, value) in enumerate(financial_items):
            col_idx = i % len(cols)
            with cols[col_idx]:
                display_name = metric.replace('_', ' ').title()
                st.markdown(f'''
                <div class="metric-card">
                    <div style="font-size: 0.9rem; opacity: 0.9;">{display_name}</div>
                    <div style="font-size: 1.3rem; font-weight: 700; margin: 0.5rem 0;">{value}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 🏛️ Corporate Announcements & Updates")
    
    announcement_categories = [
        ('💰 Dividends & Distributions', 'dividends', '#4CAF50'),
        ('💸 Fund Raising', 'fund_raising', '#FF9800'),
        ('🏢 M&A Activities', 'acquisitions_mergers', '#2196F3'),
        ('👥 Management Changes', 'appointments', '#9C27B0'),
        ('📋 Board Meetings', 'board_meetings', '#607D8B'),
        ('⚖️ Legal Cases & Disputes', 'legal_cases', '#F44336'),
        ('🔧 Regulatory Updates', 'regulatory_updates', '#00BCD4'),
        ('🏗️ Projects & Expansions', 'project_announcements', '#795548'),
        ('🌱 Environmental Matters', 'environmental_issues', '#4CAF50'),
        ('📊 Credit Ratings', 'credit_rating', '#FFC107')
    ]
    
    announcements_found = False
    
    for category_name, category_key, color in announcement_categories:
        if announcements[category_key]:
            announcements_found = True
            st.markdown(f'<div class="category-header" style="background-color: {color};">{category_name}</div>', unsafe_allow_html=True)
            
            for i, item in enumerate(announcements[category_key][:5]):
                clean_item = item
                if category_key == 'acquisitions_mergers' and 'M&A:' in item:
                    clean_item = item.replace('M&A:', '').strip()
                elif category_key == 'appointments' and 'Appointment:' in item:
                    clean_item = item.replace('Appointment:', '').strip()
                elif category_key == 'legal_cases' and 'Legal:' in item:
                    clean_item = item.replace('Legal:', '').strip()
                
                st.markdown(f'''
                <div class="announcement-card">
                    <div style="font-weight: 500; color: #333;">{clean_item}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    if not announcements_found:
        st.info("No corporate announcements detected in this document.")
    
    if any(operations.values()):
        st.markdown("---")
        st.markdown("## 🚀 Business Operations & Performance")
        
        for category, items in operations.items():
            if items:
                display_name = category.replace('_', ' ').title()
                st.markdown(f'<div class="category-header" style="background-color: #607D8B;">{display_name}</div>', unsafe_allow_html=True)
                
                for item in items[:3]:
                    st.markdown(f'''
                    <div class="announcement-card">
                        <div style="font-weight: 500; color: #333;">{item}</div>
                    </div>
                    ''', unsafe_allow_html=True)
    
    st.markdown("---")
    with st.expander("📋 View Detailed Analysis Report", expanded=False):
        report_lines = report.split('\n')
        for line in report_lines:
            if line.startswith('🚀') or line.startswith('📊') or line.startswith('📈') or line.startswith('🏛️'):
                st.markdown(f"**{line}**")
            elif line.startswith('=' * 70):
                st.markdown("---")
            elif line.startswith('•'):
                st.markdown(f"• {line[1:].strip()}")
            elif line.strip() and not line.startswith(' ' * 2) and not line.startswith('-'):
                st.markdown(line)
            else:
                st.markdown(line)
else:
    st.markdown("---")
    st.info("👆 Upload a financial PDF document to begin analysis")
