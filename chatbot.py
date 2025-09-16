import json
import os
from google import genai
from google.genai import types
import streamlit as st
from data_processor import DataProcessor
from typing import Dict, List, Any

class BudgetChatbot:
    def __init__(self, data_processor: DataProcessor):
        # Using Gemini API as requested by user - gemini-2.5-flash is the newest model
        self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.data_processor = data_processor
        self.conversation_history = []
        
    def get_response(self, user_query: str, selected_year: int = None) -> str:
        """Get AI response for user query about budget data"""
        try:
            # Search relevant data based on the query
            search_results = self.data_processor.search_data(user_query)
            
            # Get year-specific data if year is selected
            year_context = ""
            if selected_year:
                year_overview = self.data_processor.get_year_overview(selected_year)
                year_context = f"\nCurrent selected year: {selected_year}\n"
                year_context += f"Budget Summary: {json.dumps(year_overview.get('budget_summary', {}), indent=2)}\n"
                year_context += f"Top Ministries: {json.dumps(year_overview.get('top_ministries', [])[:5], indent=2)}\n"
            
            # Prepare context for AI
            context = self._prepare_context(search_results, year_context)
            
            # Create the prompt
            system_prompt = """You are an expert government budget analyst with deep knowledge of Indian fiscal policy and budget allocation patterns. You help users understand complex budget data through clear, insightful explanations.

Your responses should be:
1. Accurate and based only on the provided data
2. Clear and easy to understand for both experts and general public
3. Include specific numbers and percentages when relevant
4. Provide context and trends when possible
5. If data is not available, clearly state so

Always format numbers in Indian crore notation (e.g., ₹1,25,000 crores) and include relevant comparisons or growth rates when applicable."""

            user_prompt = f"""User Query: {user_query}

Available Data Context:
{context}

Please provide a comprehensive answer based on the available data. If the query cannot be fully answered with the provided data, explain what information is available and suggest related insights."""

            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_query})
            
            # Get AI response
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history (last 3 exchanges)
            recent_history = self.conversation_history[-6:]  # Last 3 user-assistant pairs
            messages.extend(recent_history)
            
            messages.append({"role": "user", "content": user_prompt})
            
            # Convert conversation to Gemini format
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            
            ai_response = response.text or "I apologize, but I couldn't generate a response. Please try again."
            
            # Add AI response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Keep conversation history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return ai_response
            
        except Exception as e:
            return f"I apologize, but I encountered an error processing your query: {str(e)}. Please try rephrasing your question or ask about specific budget data."
    
    def _prepare_context(self, search_results: Dict, year_context: str = "") -> str:
        """Prepare context from search results and year data"""
        context_parts = []
        
        if year_context:
            context_parts.append(year_context)
        
        # Add ministry information
        if search_results.get("ministries"):
            ministry_info = "Relevant Ministries:\n"
            for ministry in search_results["ministries"][:5]:
                ministry_info += f"- {ministry['name']}: Rank {ministry['rank']}, Latest Allocation: ₹{ministry['latest_allocation']:,.0f} crores\n"
            context_parts.append(ministry_info)
        
        # Add scheme information
        if search_results.get("schemes"):
            scheme_info = "Relevant Schemes:\n"
            for scheme in search_results["schemes"][:5]:
                scheme_info += f"- {scheme['name']} ({scheme['ministry']}): ₹{scheme['amount']:,.0f} crores in {scheme['year']}\n"
            context_parts.append(scheme_info)
        
        # Add revenue source information
        if search_results.get("revenue_sources"):
            revenue_info = "Relevant Revenue Sources:\n"
            for revenue in search_results["revenue_sources"]:
                revenue_info += f"- {revenue['source']}: ₹{revenue['latest_amount']:,.0f} crores (2025)\n"
            context_parts.append(revenue_info)
        
        # Add general budget insights
        insights = self.data_processor.get_insights_data()
        if not insights.get("error"):
            key_findings = insights.get("key_findings", [])
            if key_findings:
                context_parts.append(f"Key Budget Insights:\n" + "\n".join([f"- {finding}" for finding in key_findings[:3]]))
        
        return "\n\n".join(context_parts) if context_parts else "No specific data found for this query."
    
    def get_suggested_questions(self, selected_year: int = None) -> List[str]:
        """Get suggested questions based on current context"""
        base_questions = [
            "What are the major sources of government revenue?",
            "Which ministry receives the highest budget allocation?",
            "How has the fiscal deficit changed over the years?",
            "What are the key infrastructure spending priorities?",
            "Compare defense spending with education spending",
            "What are the major welfare schemes and their allocations?",
            "How has GST revenue performed since its introduction?",
            "What are the trends in capital vs revenue expenditure?"
        ]
        
        if selected_year:
            year_specific = [
                f"What were the budget highlights for {selected_year}?",
                f"Which schemes received major funding in {selected_year}?",
                f"How did the fiscal position change in {selected_year}?",
                f"What were the revenue growth drivers in {selected_year}?"
            ]
            return year_specific + base_questions[:4]
        
        return base_questions
    
    def analyze_budget_speech(self, year: int) -> str:
        """Analyze budget speech for a specific year"""
        try:
            speech_data = self.data_processor.speeches[
                self.data_processor.speeches['year'] == year
            ]
            
            if speech_data.empty:
                return f"No budget speech data available for {year}."
            
            speech_summary = speech_data['ai_summary'].iloc[0]
            year_overview = self.data_processor.get_year_overview(year)
            
            analysis_prompt = f"""Analyze the budget speech summary and actual budget data for {year}:

Speech Summary: {speech_summary}

Budget Data:
- Total Expenditure: ₹{year_overview.get('budget_summary', {}).get('total_expenditure', 0):,.0f} crores
- Total Receipts: ₹{year_overview.get('budget_summary', {}).get('total_receipts', 0):,.0f} crores
- Fiscal Deficit: {year_overview.get('budget_summary', {}).get('fiscal_deficit_as_gdp_pct', 0)}% of GDP

Top Ministry Allocations:
{json.dumps(year_overview.get('top_ministries', [])[:5], indent=2)}

Provide an analysis connecting the speech themes with the actual budget allocations and key policy priorities."""

            full_prompt = f"You are a budget policy analyst. Provide insights connecting budget speech themes with actual allocations.\n\n{analysis_prompt}"
            
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            
            return response.text or "Error generating analysis."
            
        except Exception as e:
            return f"Error analyzing budget speech: {str(e)}"
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history available."
        
        try:
            # Get last few exchanges
            recent_conversation = self.conversation_history[-10:]
            conversation_text = "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in recent_conversation
            ])
            
            summary_prompt = f"""Summarize the key topics and insights discussed in this budget conversation:

{conversation_text}

Provide a brief summary of the main topics covered and key insights shared."""

            full_prompt = f"Provide a concise summary of the budget discussion topics and insights.\n\n{summary_prompt}"
            
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            
            return response.text or "Error generating summary."
            
        except Exception as e:
            return f"Error generating conversation summary: {str(e)}"
