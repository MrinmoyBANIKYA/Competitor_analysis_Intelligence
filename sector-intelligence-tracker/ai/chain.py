import os
from typing import List, Literal, Dict, Any
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Pydantic Schemas ---

class NormalisedSignals(BaseModel):
    trend_score: float = Field(description="Normalized score for search interest (0-10)")
    sentiment_score: float = Field(description="Normalized score for user sentiment (0-10)")
    hiring_velocity: float = Field(description="Normalized score for hiring activity (0-10)")
    news_sentiment: float = Field(description="Normalized score for news coverage sentiment (0-10)")
    app_health: float = Field(description="Normalized score for app store performance (0-10)")

class SectorAnalysis(BaseModel):
    executive_summary: str = Field(description="High-level summary of the sector health")
    momentum_verdict: Literal['accelerating', 'stable', 'declining'] = Field(description="Current momentum trend")
    top_threats: List[str] = Field(description="List of major threats identified")
    top_opportunities: List[str] = Field(description="List of major opportunities identified")
    confidence: float = Field(description="Confidence score in this analysis (0-1)")

class StrategicRecommendations(BaseModel):
    quick_wins: List[str] = Field(description="Immediate actions to take")
    medium_term: List[str] = Field(description="Strategic moves for the next 6-12 months")
    risks: List[str] = Field(description="Key risks to monitor")
    comp_moat_assessment: str = Field(description="Assessment of competitive moats in the sector")

# --- Chain Steps ---

def get_intel_chain():
    # Model configuration
    llm_low_temp = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
    llm_high_temp = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.6)

    # Step 1: Signal Normaliser
    signal_parser = JsonOutputParser(pydantic_object=NormalisedSignals)
    signal_prompt = ChatPromptTemplate.from_template(
        "You are a data normaliser. Convert the following raw multi-source sector intelligence data into structured scores.\n"
        "Data: {raw_data}\n\n"
        "{format_instructions}"
    )
    signal_chain = signal_prompt | llm_low_temp | signal_parser

    # Step 2: Sector Analyst
    analyst_parser = JsonOutputParser(pydantic_object=SectorAnalysis)
    analyst_prompt = ChatPromptTemplate.from_template(
        "You are a Senior Sector Analyst. Based on these normalised signals and sector context, provide a deep analysis.\n"
        "Sector: {sector_context}\n"
        "Signals: {signals}\n\n"
        "{format_instructions}"
    )
    analyst_chain = analyst_prompt | llm_low_temp | analyst_parser

    # Step 3: Recommendation Engine
    rec_parser = JsonOutputParser(pydantic_object=StrategicRecommendations)
    rec_prompt = ChatPromptTemplate.from_template(
        "You are a Strategic Consultant. Based on the following sector analysis, provide actionable recommendations.\n"
        "Analysis: {analysis}\n\n"
        "{format_instructions}"
    )
    rec_chain = rec_prompt | llm_high_temp | rec_parser

    # Combining into a multi-step process
    async def run_intel_process(raw_data: Dict[str, Any], sector_context: str):
        # Step 1
        signals = await signal_chain.ainvoke({
            "raw_data": raw_data,
            "format_instructions": signal_parser.get_format_instructions()
        })
        
        # Step 2
        analysis = await analyst_chain.ainvoke({
            "sector_context": sector_context,
            "signals": signals,
            "format_instructions": analyst_parser.get_format_instructions()
        })
        
        # Step 3
        recommendations = await rec_chain.ainvoke({
            "analysis": analysis,
            "format_instructions": rec_parser.get_format_instructions()
        })
        
        return {
            "signals": signals,
            "analysis": analysis,
            "recommendations": recommendations
        }

    return run_intel_process
