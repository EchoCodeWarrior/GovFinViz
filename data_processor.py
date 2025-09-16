import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Tuple, Any
import re

class DataProcessor:
    def __init__(self):
        self.revenue_data = None
        self.expenditure_data = None
        self.budget_summary = None
        self.detailed_expenditures = None
        self.detailed_revenues = None
        self.scheme_outcomes = None
        self.speeches = None
        self.load_data()
    
    def load_data(self):
        """Load all CSV data files"""
        try:
            self.revenue_data = pd.read_csv('data/year_wise_revenue.csv')
            self.expenditure_data = pd.read_csv('data/year_wise_expenditures.csv')
            self.budget_summary = pd.read_csv('data/budget_summary.csv')
            self.detailed_expenditures = pd.read_csv('data/expenditures_detailed.csv')
            self.detailed_revenues = pd.read_csv('data/revenues_detailed.csv')
            self.scheme_outcomes = pd.read_csv('data/scheme_outcomes.csv')
            self.speeches = pd.read_csv('data/speeches.csv')
            
            # Clean and process data
            self._clean_data()
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
    
    def _clean_data(self):
        """Clean and standardize data formats"""
        # Clean revenue data - remove commas and convert to numeric
        for col in ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']:
            if col in self.revenue_data.columns:
                self.revenue_data[col] = self.revenue_data[col].astype(str).str.replace(',', '').str.replace('"', '')
                self.revenue_data[col] = pd.to_numeric(self.revenue_data[col], errors='coerce')
        
        # Clean expenditure data
        for col in ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']:
            if col in self.expenditure_data.columns:
                self.expenditure_data[col] = self.expenditure_data[col].astype(str).str.replace(',', '').str.replace('"', '')
                self.expenditure_data[col] = pd.to_numeric(self.expenditure_data[col], errors='coerce')
        
        # Clean detailed expenditures
        if 'amount_in_crores' in self.detailed_expenditures.columns:
            self.detailed_expenditures['amount_in_crores'] = pd.to_numeric(
                self.detailed_expenditures['amount_in_crores'], errors='coerce'
            )
        
        # Clean detailed revenues
        if 'amount_in_crores' in self.detailed_revenues.columns:
            self.detailed_revenues['amount_in_crores'] = pd.to_numeric(
                self.detailed_revenues['amount_in_crores'], errors='coerce'
            )
    
    def get_year_overview(self, year: int) -> Dict[str, Any]:
        """Get comprehensive overview for a specific year"""
        try:
            # Budget summary for the year
            budget_row = self.budget_summary[self.budget_summary['year'] == year]
            if budget_row.empty:
                return {"error": f"No data available for year {year}"}
            
            budget_data = budget_row.iloc[0].to_dict()
            
            # Revenue breakdown
            revenue_breakdown = self._get_revenue_for_year(year)
            
            # Top ministries by expenditure
            top_ministries = self._get_top_ministries_for_year(year)
            
            # Key schemes and expenditures
            key_schemes = self._get_key_schemes_for_year(year)
            
            # Speech summary
            speech_data = self.speeches[self.speeches['year'] == year]
            speech_summary = speech_data['ai_summary'].iloc[0] if not speech_data.empty else "No speech data available"
            
            return {
                "budget_summary": budget_data,
                "revenue_breakdown": revenue_breakdown,
                "top_ministries": top_ministries,
                "key_schemes": key_schemes,
                "speech_summary": speech_summary,
                "fiscal_health": self._calculate_fiscal_health(budget_data)
            }
        except Exception as e:
            return {"error": f"Error processing year {year}: {str(e)}"}
    
    def _get_revenue_for_year(self, year: int) -> List[Dict]:
        """Get revenue breakdown for a specific year"""
        year_col = str(year)
        if year_col not in self.revenue_data.columns:
            return []
        
        revenue_list = []
        for _, row in self.revenue_data.iterrows():
            if pd.notna(row[year_col]) and row[year_col] > 0:
                revenue_list.append({
                    "source": row['Revenue Source'],
                    "amount": row[year_col],
                    "percentage": 0  # Will be calculated later
                })
        
        # Calculate percentages
        total_revenue = sum([r['amount'] for r in revenue_list])
        for r in revenue_list:
            r['percentage'] = (r['amount'] / total_revenue * 100) if total_revenue > 0 else 0
        
        return sorted(revenue_list, key=lambda x: x['amount'], reverse=True)
    
    def _get_top_ministries_for_year(self, year: int, top_n: int = 10) -> List[Dict]:
        """Get top ministries by expenditure for a specific year"""
        year_col = str(year)
        if year_col not in self.expenditure_data.columns:
            return []
        
        ministries = []
        for _, row in self.expenditure_data.iterrows():
            if pd.notna(row[year_col]) and row[year_col] > 0:
                ministries.append({
                    "ministry": row['Ministry Name'],
                    "amount": row[year_col],
                    "rank": row.get('Rank', 0)
                })
        
        return sorted(ministries, key=lambda x: x['amount'], reverse=True)[:top_n]
    
    def _get_key_schemes_for_year(self, year: int) -> List[Dict]:
        """Get key schemes and expenditures for a specific year"""
        year_schemes = self.detailed_expenditures[self.detailed_expenditures['year'] == year]
        
        schemes = []
        for _, row in year_schemes.iterrows():
            schemes.append({
                "ministry": row['ministry_name'],
                "scheme": row['grant_or_scheme_name'],
                "amount": row['amount_in_crores'],
                "type": row['expenditure_type'],
                "estimate_type": row['estimate_type']
            })
        
        return sorted(schemes, key=lambda x: x['amount'], reverse=True)
    
    def _calculate_fiscal_health(self, budget_data: Dict) -> Dict:
        """Calculate fiscal health indicators"""
        try:
            total_receipts = budget_data.get('total_receipts', 0)
            total_expenditure = budget_data.get('total_expenditure', 0)
            gdp = budget_data.get('gdp_nominal_in_crores', 0)
            fiscal_deficit = budget_data.get('fiscal_deficit_in_crores', 0)
            
            return {
                "budget_balance": total_receipts - total_expenditure,
                "expenditure_to_gdp": (total_expenditure / gdp * 100) if gdp > 0 else 0,
                "revenue_to_gdp": (total_receipts / gdp * 100) if gdp > 0 else 0,
                "fiscal_deficit_ratio": budget_data.get('fiscal_deficit_as_gdp_pct', 0),
                "deficit_trend": self._get_deficit_trend(budget_data['year'])
            }
        except Exception as e:
            return {"error": f"Error calculating fiscal health: {str(e)}"}
    
    def _get_deficit_trend(self, current_year: int) -> str:
        """Analyze fiscal deficit trend"""
        try:
            current_deficit = self.budget_summary[self.budget_summary['year'] == current_year]['fiscal_deficit_as_gdp_pct'].iloc[0]
            previous_year_data = self.budget_summary[self.budget_summary['year'] == current_year - 1]
            
            if not previous_year_data.empty:
                previous_deficit = previous_year_data['fiscal_deficit_as_gdp_pct'].iloc[0]
                if current_deficit < previous_deficit:
                    return "Improving"
                elif current_deficit > previous_deficit:
                    return "Deteriorating"
                else:
                    return "Stable"
            return "No trend data"
        except:
            return "Unknown"
    
    def get_ministry_details(self, year: int, ministry_name: str) -> Dict:
        """Get detailed information about a specific ministry"""
        try:
            year_col = str(year)
            ministry_row = self.expenditure_data[
                (self.expenditure_data['Ministry Name'].str.contains(ministry_name, case=False, na=False)) &
                (self.expenditure_data[year_col].notna())
            ]
            
            if ministry_row.empty:
                return {"error": f"No data found for {ministry_name} in {year}"}
            
            ministry_data = ministry_row.iloc[0]
            
            # Get historical trend
            historical_data = []
            for yr in range(2016, 2026):
                yr_col = str(yr)
                if yr_col in ministry_data and pd.notna(ministry_data[yr_col]):
                    historical_data.append({
                        "year": yr,
                        "amount": ministry_data[yr_col]
                    })
            
            # Get specific schemes for this ministry and year
            ministry_schemes = self.detailed_expenditures[
                (self.detailed_expenditures['year'] == year) &
                (self.detailed_expenditures['ministry_name'].str.contains(ministry_name, case=False, na=False))
            ]
            
            schemes = []
            for _, scheme in ministry_schemes.iterrows():
                schemes.append({
                    "scheme": scheme['grant_or_scheme_name'],
                    "amount": scheme['amount_in_crores'],
                    "type": scheme['expenditure_type']
                })
            
            return {
                "ministry_name": ministry_data['Ministry Name'],
                "current_allocation": ministry_data[year_col],
                "rank": ministry_data.get('Rank', 0),
                "historical_trend": historical_data,
                "major_schemes": schemes,
                "total_10_year": ministry_data.get('10-Year Total', 'N/A')
            }
        except Exception as e:
            return {"error": f"Error processing ministry data: {str(e)}"}
    
    def get_comparison_data(self, years: List[int]) -> Dict:
        """Get comparison data for multiple years"""
        try:
            comparison = {
                "years": years,
                "budget_summary": [],
                "revenue_comparison": {},
                "expenditure_comparison": {},
                "ministry_trends": {}
            }
            
            # Budget summary comparison
            for year in years:
                year_data = self.budget_summary[self.budget_summary['year'] == year]
                if not year_data.empty:
                    comparison["budget_summary"].append(year_data.iloc[0].to_dict())
            
            # Revenue comparison
            for revenue_source in self.revenue_data['Revenue Source']:
                source_data = []
                revenue_row = self.revenue_data[self.revenue_data['Revenue Source'] == revenue_source]
                if not revenue_row.empty:
                    for year in years:
                        year_col = str(year)
                        if year_col in revenue_row.columns:
                            amount = revenue_row[year_col].iloc[0]
                            if pd.notna(amount):
                                source_data.append({"year": year, "amount": amount})
                    if source_data:
                        comparison["revenue_comparison"][revenue_source] = source_data
            
            # Top 10 ministries comparison
            top_ministries = self.expenditure_data.head(10)['Ministry Name'].tolist()
            for ministry in top_ministries:
                ministry_row = self.expenditure_data[self.expenditure_data['Ministry Name'] == ministry]
                if not ministry_row.empty:
                    ministry_data = []
                    for year in years:
                        year_col = str(year)
                        if year_col in ministry_row.columns:
                            amount = ministry_row[year_col].iloc[0]
                            if pd.notna(amount):
                                ministry_data.append({"year": year, "amount": amount})
                    if ministry_data:
                        comparison["ministry_trends"][ministry] = ministry_data
            
            return comparison
        except Exception as e:
            return {"error": f"Error creating comparison: {str(e)}"}
    
    def get_insights_data(self) -> Dict:
        """Generate insights from the budget data"""
        try:
            insights = {
                "revenue_trends": self._analyze_revenue_trends(),
                "expenditure_patterns": self._analyze_expenditure_patterns(),
                "fiscal_analysis": self._analyze_fiscal_trends(),
                "ministry_performance": self._analyze_ministry_performance(),
                "key_findings": self._generate_key_findings()
            }
            return insights
        except Exception as e:
            return {"error": f"Error generating insights: {str(e)}"}
    
    def _analyze_revenue_trends(self) -> Dict:
        """Analyze revenue trends across years"""
        trends = {}
        
        # Calculate year-over-year growth for major revenue sources
        major_sources = ['Corporation Tax', 'Income Tax', 'Goods and Services Tax (GST)']
        
        for source in major_sources:
            source_row = self.revenue_data[self.revenue_data['Revenue Source'] == source]
            if not source_row.empty:
                source_data = source_row.iloc[0]
                growth_rates = []
                
                for i, year in enumerate(range(2017, 2026)):
                    current_year = str(year)
                    previous_year = str(year - 1)
                    
                    if current_year in source_data and previous_year in source_data:
                        current_val = source_data[current_year]
                        previous_val = source_data[previous_year]
                        
                        if pd.notna(current_val) and pd.notna(previous_val) and previous_val > 0:
                            growth_rate = ((current_val - previous_val) / previous_val) * 100
                            growth_rates.append({
                                "year": year,
                                "growth_rate": growth_rate
                            })
                
                trends[source] = {
                    "growth_rates": growth_rates,
                    "avg_growth": np.mean([g['growth_rate'] for g in growth_rates]) if growth_rates else 0
                }
        
        return trends
    
    def _analyze_expenditure_patterns(self) -> Dict:
        """Analyze expenditure patterns"""
        patterns = {}
        
        # Calculate total expenditure by year
        yearly_totals = []
        for year in range(2016, 2026):
            year_col = str(year)
            if year_col in self.expenditure_data.columns:
                total = self.expenditure_data[year_col].sum()
                yearly_totals.append({"year": year, "total": total})
        
        patterns["yearly_totals"] = yearly_totals
        
        # Top growing ministries
        growth_rates = {}
        for _, ministry in self.expenditure_data.iterrows():
            ministry_name = ministry['Ministry Name']
            
            # Calculate growth from 2016 to 2025
            start_val = ministry.get('2016', 0)
            end_val = ministry.get('2025', 0)
            
            if pd.notna(start_val) and pd.notna(end_val) and start_val > 0:
                growth_rate = ((end_val - start_val) / start_val) * 100
                growth_rates[ministry_name] = growth_rate
        
        # Sort by growth rate
        sorted_growth = sorted(growth_rates.items(), key=lambda x: x[1], reverse=True)
        patterns["top_growing_ministries"] = sorted_growth[:10]
        patterns["declining_ministries"] = sorted_growth[-5:]
        
        return patterns
    
    def _analyze_fiscal_trends(self) -> Dict:
        """Analyze fiscal health trends"""
        fiscal_data = []
        
        for _, row in self.budget_summary.iterrows():
            fiscal_data.append({
                "year": row['year'],
                "fiscal_deficit_ratio": row['fiscal_deficit_as_gdp_pct'],
                "expenditure_to_gdp": (row['total_expenditure'] / row['gdp_nominal_in_crores']) * 100,
                "revenue_to_gdp": (row['total_receipts'] / row['gdp_nominal_in_crores']) * 100
            })
        
        # Calculate averages
        avg_deficit = np.mean([d['fiscal_deficit_ratio'] for d in fiscal_data])
        avg_exp_gdp = np.mean([d['expenditure_to_gdp'] for d in fiscal_data])
        
        return {
            "yearly_data": fiscal_data,
            "average_deficit_ratio": avg_deficit,
            "average_expenditure_to_gdp": avg_exp_gdp,
            "trend_analysis": self._classify_fiscal_trend(fiscal_data)
        }
    
    def _classify_fiscal_trend(self, fiscal_data: List[Dict]) -> str:
        """Classify the overall fiscal trend"""
        recent_years = sorted(fiscal_data, key=lambda x: x['year'])[-3:]
        early_years = sorted(fiscal_data, key=lambda x: x['year'])[:3]
        
        recent_avg = np.mean([y['fiscal_deficit_ratio'] for y in recent_years])
        early_avg = np.mean([y['fiscal_deficit_ratio'] for y in early_years])
        
        if recent_avg < early_avg - 0.5:
            return "Improving fiscal health"
        elif recent_avg > early_avg + 0.5:
            return "Deteriorating fiscal health"
        else:
            return "Stable fiscal health"
    
    def _analyze_ministry_performance(self) -> Dict:
        """Analyze ministry allocation patterns"""
        # Calculate average allocation per ministry
        ministry_stats = {}
        
        for _, ministry in self.expenditure_data.iterrows():
            ministry_name = ministry['Ministry Name']
            
            # Calculate total allocation and consistency
            allocations = []
            for year in range(2016, 2026):
                year_col = str(year)
                if year_col in ministry and pd.notna(ministry[year_col]):
                    allocations.append(ministry[year_col])
            
            if allocations:
                ministry_stats[ministry_name] = {
                    "average_allocation": np.mean(allocations),
                    "total_allocation": sum(allocations),
                    "allocation_variance": np.var(allocations),
                    "consistency_score": 1 / (1 + np.var(allocations) / np.mean(allocations)) if np.mean(allocations) > 0 else 0
                }
        
        # Sort by different metrics
        by_total = sorted(ministry_stats.items(), key=lambda x: x[1]['total_allocation'], reverse=True)
        by_consistency = sorted(ministry_stats.items(), key=lambda x: x[1]['consistency_score'], reverse=True)
        
        return {
            "top_by_total": by_total[:10],
            "most_consistent": by_consistency[:10],
            "ministry_statistics": ministry_stats
        }
    
    def _generate_key_findings(self) -> List[str]:
        """Generate key findings from the data analysis"""
        findings = []
        
        # Revenue findings
        gst_data = self.revenue_data[self.revenue_data['Revenue Source'] == 'Goods and Services Tax (GST)']
        if not gst_data.empty:
            gst_2025 = gst_data['2025'].iloc[0] if pd.notna(gst_data['2025'].iloc[0]) else 0
            gst_2017 = gst_data['2017'].iloc[0] if pd.notna(gst_data['2017'].iloc[0]) else 0
            if gst_2017 > 0:
                gst_growth = ((gst_2025 - gst_2017) / gst_2017) * 100
                findings.append(f"GST revenue has grown by {gst_growth:.1f}% since its introduction in 2017")
        
        # Defense spending
        defense_data = self.expenditure_data[self.expenditure_data['Ministry Name'] == 'Ministry of Defence']
        if not defense_data.empty:
            def_2025 = defense_data['2025'].iloc[0] if pd.notna(defense_data['2025'].iloc[0]) else 0
            def_2016 = defense_data['2016'].iloc[0] if pd.notna(defense_data['2016'].iloc[0]) else 0
            if def_2016 > 0:
                def_growth = ((def_2025 - def_2016) / def_2016) * 100
                findings.append(f"Defense spending has increased by {def_growth:.1f}% over the decade")
        
        # Fiscal deficit trend
        recent_deficit = self.budget_summary[self.budget_summary['year'] == 2025]['fiscal_deficit_as_gdp_pct'].iloc[0]
        findings.append(f"The fiscal deficit for 2025 is projected at {recent_deficit}% of GDP")
        
        # Top ministry
        top_ministry = self.expenditure_data.iloc[0]['Ministry Name']
        findings.append(f"Ministry of Finance consistently remains the largest spender across all years")
        
        return findings
    
    def search_data(self, query: str) -> Dict:
        """Search across all data for relevant information"""
        results = {
            "ministries": [],
            "schemes": [],
            "revenue_sources": [],
            "insights": []
        }
        
        query_lower = query.lower()
        
        # Search ministries
        ministry_matches = self.expenditure_data[
            self.expenditure_data['Ministry Name'].str.contains(query, case=False, na=False)
        ]
        for _, ministry in ministry_matches.iterrows():
            results["ministries"].append({
                "name": ministry['Ministry Name'],
                "rank": ministry.get('Rank', 0),
                "latest_allocation": ministry.get('2025', 0)
            })
        
        # Search schemes
        scheme_matches = self.detailed_expenditures[
            self.detailed_expenditures['grant_or_scheme_name'].str.contains(query, case=False, na=False)
        ]
        for _, scheme in scheme_matches.iterrows():
            results["schemes"].append({
                "name": scheme['grant_or_scheme_name'],
                "ministry": scheme['ministry_name'],
                "amount": scheme['amount_in_crores'],
                "year": scheme['year']
            })
        
        # Search revenue sources
        revenue_matches = self.revenue_data[
            self.revenue_data['Revenue Source'].str.contains(query, case=False, na=False)
        ]
        for _, revenue in revenue_matches.iterrows():
            results["revenue_sources"].append({
                "source": revenue['Revenue Source'],
                "latest_amount": revenue.get('2025', 0)
            })
        
        return results
