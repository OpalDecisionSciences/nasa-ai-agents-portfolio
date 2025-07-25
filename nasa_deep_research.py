"""
NASA Deep Research Agent
Advanced research agent specialized for space missions, technical analysis, and NASA-related topics
"""

import gradio as gr
import asyncio
import openai
from typing import AsyncIterator, List, Dict
import json
import os
from datetime import datetime

class NASAResearchAgent:
    def __init__(self):
        self.client = openai.AsyncOpenAI()
        self.research_domains = {
            "mission_planning": "Space mission design, trajectory analysis, and mission architecture",
            "propulsion": "Rocket engines, spacecraft propulsion systems, and fuel efficiency",
            "materials": "Space-grade materials, thermal protection, and structural composites",
            "life_support": "Environmental control, life support systems, and crew safety",
            "exploration": "Planetary exploration, rovers, landers, and scientific instruments",
            "communications": "Deep space communications, satellite networks, and data transmission"
        }
    
    async def analyze_research_domain(self, query: str) -> str:
        """Determine the most relevant NASA research domain for the query"""
        prompt = f"""
        Analyze this research query and determine which NASA domain it best fits:
        Query: {query}
        
        Domains:
        {json.dumps(self.research_domains, indent=2)}
        
        Return only the domain key (e.g., 'mission_planning').
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        
        domain = response.choices[0].message.content.strip().strip('"\'')
        return domain if domain in self.research_domains else "exploration"
    
    async def generate_research_questions(self, query: str, domain: str) -> List[str]:
        """Generate NASA-specific research questions"""
        prompt = f"""
        As a NASA research specialist in {self.research_domains[domain]}, generate 5 specific, 
        technical research questions related to: {query}
        
        Focus on:
        - Current NASA missions and programs
        - Technical challenges and solutions
        - Future mission requirements
        - Safety and reliability considerations
        - Cost-effectiveness and efficiency
        
        Return as a JSON list of strings.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        try:
            questions = json.loads(response.choices[0].message.content)
            return questions
        except:
            return [query]  # Fallback
    
    async def research_question(self, question: str, domain: str) -> str:
        """Research a specific question with NASA focus"""
        prompt = f"""
        As a NASA technical expert in {self.research_domains[domain]}, provide a comprehensive 
        analysis of: {question}
        
        Include:
        - Current state of technology/knowledge
        - NASA's current approach and missions
        - Technical challenges and constraints
        - Recent developments and innovations
        - Future implications for space exploration
        - Specific NASA programs, missions, or initiatives
        
        Use technical accuracy appropriate for NASA engineers and scientists.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    async def synthesize_report(self, query: str, domain: str, research_results: List[str]) -> str:
        """Create final NASA research report"""
        prompt = f"""
        Create a comprehensive NASA research report on: {query}
        
        Domain: {self.research_domains[domain]}
        
        Research findings:
        {chr(10).join(f"Section {i+1}: {result}" for i, result in enumerate(research_results))}
        
        Format as a professional NASA technical report with:
        1. Executive Summary
        2. Technical Analysis
        3. Current NASA Activities
        4. Challenges and Opportunities
        5. Recommendations
        6. Future Research Directions
        
        Use NASA terminology and reference real NASA programs where applicable.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        
        return response.choices[0].message.content

    async def run_research(self, query: str) -> AsyncIterator[str]:
        """Main research pipeline"""
        yield f"🚀 NASA Deep Research Agent Activated\n\n"
        yield f"**Research Query:** {query}\n\n"
        
        # Determine domain
        yield "🔍 Analyzing research domain...\n"
        domain = await self.analyze_research_domain(query)
        yield f"**Domain:** {self.research_domains[domain]}\n\n"
        
        # Generate research questions
        yield "📋 Generating research questions...\n"
        questions = await self.generate_research_questions(query, domain)
        yield f"**Research Questions Generated:** {len(questions)}\n\n"
        
        # Research each question
        research_results = []
        for i, question in enumerate(questions, 1):
            yield f"🔬 Researching question {i}/{len(questions)}: {question[:100]}...\n"
            result = await self.research_question(question, domain)
            research_results.append(result)
            yield f"✅ Question {i} completed\n\n"
        
        # Synthesize final report
        yield "📊 Synthesizing final NASA research report...\n\n"
        final_report = await self.synthesize_report(query, domain, research_results)
        
        yield "🎯 **NASA RESEARCH REPORT COMPLETE**\n\n"
        yield final_report

# Gradio Interface
async def run_nasa_research(query: str):
    """Run NASA research and yield results"""
    agent = NASAResearchAgent()
    async for chunk in agent.run_research(query):
        yield chunk

# Create Gradio interface
with gr.Blocks(
    title="NASA Deep Research Agent",
    theme=gr.themes.Base(
        primary_hue="blue",
        secondary_hue="orange"
    ).set(
        body_background_fill="linear-gradient(45deg, #0f1419, #1a237e)",
        panel_background_fill="rgba(255,255,255,0.05)"
    )
) as demo:
    
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #ffffff; font-size: 2.5em; margin-bottom: 10px;">
            🚀 NASA Deep Research Agent
        </h1>
        <p style="color: #cccccc; font-size: 1.2em;">
            Advanced AI research system for space missions and NASA technologies
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            query_input = gr.Textbox(
                label="Research Query",
                placeholder="e.g., 'Mars mission life support systems', 'James Webb Space Telescope innovations', 'Lunar base construction materials'",
                lines=3
            )
            
            research_button = gr.Button(
                "🚀 Start NASA Research",
                variant="primary",
                size="lg"
            )
            
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ffffff;">Research Domains</h3>
                <ul style="color: #cccccc;">
                    <li>🛰️ Mission Planning</li>
                    <li>🚀 Propulsion Systems</li>
                    <li>🔬 Space Materials</li>
                    <li>🌱 Life Support</li>
                    <li>🌍 Planetary Exploration</li>
                    <li>📡 Communications</li>
                </ul>
            </div>
            """)
    
    report_output = gr.Markdown(
        label="NASA Research Report",
        value="Ready to conduct NASA-level research. Enter your query above.",
        container=True
    )
    
    # Event handlers
    research_button.click(
        fn=run_nasa_research,
        inputs=query_input,
        outputs=report_output
    )
    
    query_input.submit(
        fn=run_nasa_research,
        inputs=query_input,
        outputs=report_output
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        inbrowser=True
    )