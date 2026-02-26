import pandas as pd
import re
import requests
import json
import matplotlib
matplotlib.use('Agg') # This is the crucial fix for threading errors
import matplotlib.pyplot as plt
import os
import time

class Aquabot:
    """
    A chatbot that can answer questions about groundwater data and generate graphs for multiple metrics.
    """
    def __init__(self, district_data, block_data, yearly_data, availability_data):
        self.district_data = district_data
        self.block_data = block_data
        self.yearly_data = yearly_data
        self.availability_data = availability_data
        
        # Prepare dataframes
        self.district_data.columns = self.district_data.columns.str.strip()
        self.districts = self.district_data['Name of District'].str.lower().str.strip().tolist()
        self.block_data.columns = self.block_data.columns.str.strip()
        self.block_data['block_lower'] = self.block_data['block'].str.lower().str.strip()
        self.block_data['district_lower'] = self.block_data['District'].str.lower().str.strip()
        self.yearly_data.columns = self.yearly_data.columns.str.strip()
        self.yearly_data['District_lower'] = self.yearly_data['District'].str.lower().str.strip()
        self.availability_data.columns = self.availability_data.columns.str.strip()
        self.availability_data['District_lower'] = self.availability_data['District'].str.lower().str.strip()

        
        self.api_key = ""
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={self.api_key}"

    def _generate_recharge_graph(self, district_name):
        """Generates and saves a recharge graph for a specific district."""
        try:
            district_yearly_data = self.yearly_data[self.yearly_data['District_lower'] == district_name.lower()]
            if district_yearly_data.empty:
                return {"answer": f"I'm sorry, I couldn't find any yearly recharge data for '{district_name}' to plot."}

            data_to_plot = district_yearly_data.iloc[0]
            
            year_columns = [col for col in self.yearly_data.columns if re.search(r'\b(20\d{2})\b', col)]
            years = [re.search(r'\b(20\d{2})\b', col).group(1) for col in year_columns]
            values = [data_to_plot[col] for col in year_columns]

            plt.style.use('seaborn-v0_8-whitegrid')
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ax.plot(years, values, marker='o', linestyle='-', color='b', label=f'Recharge for {district_name.title()}')
            ax.set_title(f'Total Annual Ground Water Recharge in {district_name.title()}', fontsize=16)
            ax.set_xlabel('Year', fontsize=12)
            ax.set_ylabel('Total Recharge (ham)', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.legend()
            plt.tight_layout()

            if not os.path.exists('static/plots'):
                os.makedirs('static/plots')
                
            timestamp = int(time.time())
            filename = f'static/plots/recharge_{district_name.lower().replace(" ", "_")}_{timestamp}.png'
            plt.savefig(filename)
            plt.close(fig)
            
            return {"graph_url": f'/{filename}'}
        except Exception as e:
            print(f"Error generating recharge graph: {e}")
            return {"answer": "I'm sorry, something went wrong while creating the recharge graph."}

    def _generate_availability_graph(self, district_name):
        """Generates and saves a future availability graph for a specific district."""
        try:
            district_availability_data = self.availability_data[self.availability_data['District_lower'] == district_name.lower()]
            if district_availability_data.empty:
                return {"answer": f"I'm sorry, I couldn't find any yearly availability data for '{district_name}' to plot."}

            data_to_plot = district_availability_data.iloc[0]
            
            year_columns = [col for col in self.availability_data.columns if re.search(r'\b(20\d{2})\b', col)]
            years = [re.search(r'\b(20\d{2})\b', col).group(1) for col in year_columns]
            values = [data_to_plot[col] for col in year_columns]

            plt.style.use('seaborn-v0_8-whitegrid')
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ax.plot(years, values, marker='s', linestyle='--', color='g', label=f'Availability for {district_name.title()}')
            ax.set_title(f'Net Ground Water Availability For Future Use in {district_name.title()}', fontsize=16)
            ax.set_xlabel('Year', fontsize=12)
            ax.set_ylabel('Net Availability (ham)', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.legend()
            plt.tight_layout()

            if not os.path.exists('static/plots'):
                os.makedirs('static/plots')
                
            timestamp = int(time.time())
            filename = f'static/plots/availability_{district_name.lower().replace(" ", "_")}_{timestamp}.png'
            plt.savefig(filename)
            plt.close(fig)
            
            return {"graph_url": f'/{filename}'}
        except Exception as e:
            print(f"Error generating availability graph: {e}")
            return {"answer": "I'm sorry, something went wrong while creating the availability graph."}

    # Helper functions to generate specific report sections
    def _get_recharge_details(self, district_data):
        return f"""Here are the **Recharge Details** for **{district_data['Name of District']}**:

--- **Recharge Details** ---
- **From Rainfall (Monsoon):** {district_data['Recharge from rainfall (Monsoon)']}
- **From Other Sources (Monsoon):** {district_data['Recharge from other sources (Monsoon)']}
- **From Rainfall (Non-Monsoon):** {district_data['Recharge from rainfall (Non-monsoon)']}
- **From Other Sources (Non-Monsoon):** {district_data['Recharge from other sources (Non-monsoon)']}"""

    def _get_availability_details(self, district_data):
        return f"""Here is the **Overall Availability** for **{district_data['Name of District']}**:

--- **Overall Availability** ---
- **Total Annual Recharge:** {district_data['Total Annual Ground Water Recharge']}
- **Total Natural Discharges:** {district_data['Total Natural Discharges']}
- **Annual Extractable Resource:** {district_data['Annual Extractable Ground Water Resource']}
- **Net Availability for Future Use:** {district_data['Net Ground Water Availability for future use']}"""

    def _get_extraction_details(self, district_data):
        return f"""Here are the **Extraction Details** for **{district_data['Name of District']}**:

--- **Extraction Details** ---
- **Irrigation:** {district_data['Irrigation']} ham
- **Industrial:** {district_data['Industrial']}
- **Domestic:** {district_data['Domestic']}
- **Total Extraction:** {district_data['Total']}"""

    def _get_status_details(self, district_data):
        return f"""Here is the **Status** for **{district_data['Name of District']}**:

--- **Status** ---
- **Stage of Extraction (%):** {district_data['Stage of Ground Water Extraction (%)']}%
- **Projected Domestic Allocation (2025):** {district_data['Annual GW Allocation for Domestic Use as on 2025']}"""

    def answer_question(self, question):
        """Analyzes a user's question and returns an appropriate answer."""
        question_lower = question.lower().strip()

        # Check for graph requests first
        if any(keyword in question_lower for keyword in ['plot', 'graph', 'chart']):
            district_match = None
            for district in self.districts:
                if re.search(r'\b' + re.escape(district) + r'\b', question_lower):
                    district_match = district
                    break
            
            if not district_match:
                return {"answer": "I can plot data, but you need to specify which district."}

            if 'recharge' in question_lower:
                return self._generate_recharge_graph(district_match)
            if 'availability' in question_lower or 'future use' in question_lower:
                return self._generate_availability_graph(district_match)
            
            return {"answer": f"I can generate a graph for '{district_match.title()}', but please specify what you want to plot (e.g., 'recharge' or 'availability')."}

        # Text-based queries
        found_district = None
        for district in self.districts:
            if re.search(r'\b' + re.escape(district) + r'\b', question_lower):
                found_district = district
                break
        
        if found_district:
            district_data = self.district_data[self.district_data['Name of District'].str.lower().str.strip() == found_district].iloc[0]

            # Section-specific queries
            if 'recharge detail' in question_lower or 'recharge data' in question_lower:
                return {"answer": self._get_recharge_details(district_data)}
            if 'availability' in question_lower:
                return {"answer": self._get_availability_details(district_data)}
            if 'extraction detail' in question_lower or 'extraction data' in question_lower:
                return {"answer": self._get_extraction_details(district_data)}
            if 'status' in question_lower:
                return {"answer": self._get_status_details(district_data)}

            # Block-level queries
            if 'block' in question_lower:
                possible_blocks = self.block_data[self.block_data['district_lower'] == found_district]
                for _, row in possible_blocks.iterrows():
                    if re.search(r'\b' + re.escape(row['block_lower']) + r'\b', question_lower):
                        return {"answer": f"The condition of the **{row['block']}** block in **{row['District']}** is: **{row['Condition 2024']}**."}
                return {"answer": f"I can't find that specific block in {found_district.title()}. Please check the name."}
            
            # Fallback to the complete report
            report = f"""Here is the comprehensive report for **{district_data['Name of District']}**:

{self._get_recharge_details(district_data).split('---', 1)[1].strip()}

{self._get_availability_details(district_data).split('---', 1)[1].strip()}

{self._get_extraction_details(district_data).split('---', 1)[1].strip()}

{self._get_status_details(district_data).split('---', 1)[1].strip()}

You can also ask about a specific block (e.g., 'What is the condition of Achhnera block?')."""
            return {"answer": report}

        return {"answer": "I can help with that. Please specify a district. For graphs, ask something like 'plot recharge for Agra' or 'graph availability for Varanasi'."}

