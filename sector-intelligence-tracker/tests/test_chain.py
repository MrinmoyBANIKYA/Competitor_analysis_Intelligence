import pytest
import os
import json
from unittest.mock import AsyncMock, patch
from langchain_core.messages import AIMessage

# Set dummy API key for tests
os.environ["GOOGLE_API_KEY"] = "dummy_key"

from ai.chain import get_intel_chain

@pytest.mark.asyncio
async def test_intel_chain_logic():
    # Mock data
    mock_raw_data = {"test": "data"}
    mock_sector = "Fintech"
    
    # Mock return values for each step
    mock_signals = {
        "trend_score": 8.5,
        "sentiment_score": 7.0,
        "hiring_velocity": 9.0,
        "news_sentiment": 6.5,
        "app_health": 8.0
    }
    mock_analysis = {
        "executive_summary": "Sector is growing rapidly.",
        "momentum_verdict": "accelerating",
        "top_threats": ["Regulation"],
        "top_opportunities": ["AI Integration"],
        "confidence": 0.95
    }
    mock_recs = {
        "quick_wins": ["Update app"],
        "medium_term": ["Expand to SEA"],
        "risks": ["Competition"],
        "comp_moat_assessment": "High switching costs."
    }

    # We need to mock ChatGoogleGenerativeAI's ainvoke
    with patch("ai.chain.ChatGoogleGenerativeAI.ainvoke") as mock_ainvoke:
        # Step 1, 2, and 3 mock responses as AIMessages with JSON strings
        mock_ainvoke.side_effect = [
            AIMessage(content=json.dumps(mock_signals)),
            AIMessage(content=json.dumps(mock_analysis)),
            AIMessage(content=json.dumps(mock_recs))
        ]
        
        run_process = get_intel_chain()
        result = await run_process(mock_raw_data, mock_sector)
        
        assert result["signals"] == mock_signals
        assert result["analysis"] == mock_analysis
        assert result["recommendations"] == mock_recs
        assert mock_ainvoke.call_count == 3

@pytest.mark.asyncio
async def test_signal_normalization_schema():
    # Test if the chain correctly uses the Pydantic schema (logic test)
    # This is more of a smoke test for the structure
    run_process = get_intel_chain()
    assert callable(run_process)
