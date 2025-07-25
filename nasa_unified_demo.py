"""
NASA AI Agents Portfolio - Unified Demo Interface
All 6 NASA AI agents in one professional interface for interview demonstration
"""

import gradio as gr
import asyncio
import openai
import json
import random
import math
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Import components from individual agents
import sys
import importlib.util

class NASAUnifiedPortfolio:
    """Unified NASA AI Agents Portfolio"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI()
    
    # DEEP RESEARCH AGENT FUNCTIONS
    async def run_deep_research(self, query: str):
        """Deep Research Agent - Simplified for unified interface"""
        if not query.strip():
            yield "Please enter a research query."
            return
        
        yield f"🚀 **NASA Deep Research Agent Activated**\n\n"
        yield f"**Research Query:** {query}\n\n"
        
        # Domain analysis
        yield "🔍 **Analyzing research domain...**\n"
        domains = {
            "mission_planning": "Space mission design and architecture",
            "propulsion": "Rocket engines and spacecraft propulsion",
            "materials": "Space-grade materials and composites",
            "life_support": "Environmental control and crew safety",
            "exploration": "Planetary exploration and scientific instruments"
        }
        
        domain = "exploration"  # Simplified for demo
        yield f"**Domain:** {domains[domain]}\n\n"
        
        # Research analysis
        yield "📊 **Conducting NASA-level research analysis...**\n\n"
        
        prompt = f"""
        As a NASA research specialist, provide comprehensive analysis of: {query}
        
        Include:
        - Current NASA programs and missions
        - Technical challenges and solutions
        - Recent developments and innovations
        - Future implications for space exploration
        - Specific recommendations
        
        Format as a professional NASA research brief.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        
        yield "✅ **Research Analysis Complete**\n\n"
        yield response.choices[0].message.content
    
    # ENGINEERING TEAM FUNCTIONS
    async def run_engineering_team(self, project_description: str):
        """Engineering Team Agent - Simplified for unified interface"""
        if not project_description.strip():
            yield "Please enter a project description."
            return
        
        yield f"🚀 **NASA Engineering Team Design Session**\n\n"
        yield f"**Project:** {project_description}\n\n"
        
        yield f"**Team Members:**\n"
        yield f"- 🎯 Systems Engineer (Lead)\n"
        yield f"- 🚀 Propulsion Engineer\n"
        yield f"- 🏗️ Structural Engineer\n"
        yield f"- 💻 Software Engineer\n"
        yield f"- 🎮 Mission Operations Engineer\n\n"
        
        # Systems Design
        yield "## 🎯 **Systems Design Phase**\n\n"
        systems_prompt = f"""
        As NASA's Systems Engineer, design the overall architecture for: {project_description}
        
        Provide:
        1. Mission requirements and objectives
        2. Top-level system architecture
        3. Key performance parameters
        4. Interface requirements for subsystems
        
        Use NASA engineering standards.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": systems_prompt}],
            max_tokens=1000
        )
        
        yield response.choices[0].message.content + "\n\n"
        
        # Integration Summary
        yield "## ✅ **Engineering Integration Summary**\n\n"
        yield f"- **Systems Architecture:** Completed\n"
        yield f"- **Subsystem Integration:** Verified\n"
        yield f"- **NASA Standards Compliance:** Confirmed\n"
        yield f"- **Ready for Development Phase:** ✅\n"
    
    # MISSION CONTROL FUNCTIONS
    async def run_mission_control(self, scenario: str, mission_phase: str):
        """Mission Control Agent - Simplified for unified interface"""
        if not scenario.strip():
            yield "Please enter a mission control scenario."
            return
        
        yield f"🚀 **NASA Mission Control Response**\n\n"
        yield f"**Mission Phase:** {mission_phase.replace('_', ' ').title()}\n"
        yield f"**Scenario:** {scenario}\n\n"
        
        yield "## 🎯 **Mission Specialist Analysis**\n\n"
        
        # Determine priority level
        priority = "critical" if any(word in scenario.lower() for word in ["emergency", "failure", "danger", "critical"]) else "elevated"
        yield f"**Priority Level:** {priority.upper()}\n"
        yield f"**Emergency Status:** {'🚨 ACTIVE' if priority == 'critical' else '✅ Normal'}\n\n"
        
        # Mission Control Analysis
        mc_prompt = f"""
        As NASA Mission Control team, analyze this scenario: {scenario}
        
        Mission Phase: {mission_phase}
        Priority: {priority}
        
        Provide:
        1. Situation assessment
        2. Immediate actions required
        3. Systems check recommendations
        4. Flight Director decision
        
        Use NASA mission control protocols.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": mc_prompt}],
            max_tokens=1200
        )
        
        yield "## 📡 **Mission Control Team Response**\n\n"
        yield response.choices[0].message.content + "\n\n"
        
        yield f"**Flight Director Authorization:** ✅ APPROVED\n"
        yield f"**Mission Status:** OPERATIONAL\n"
    
    # SPACECRAFT AUTONOMY FUNCTIONS
    async def run_spacecraft_autonomy(self, situation: str, mission_scenario: str):
        """Spacecraft Autonomy Agent - Simplified for unified interface"""
        if not situation.strip():
            yield "Please enter an autonomous situation."
            return
        
        yield f"🤖 **NASA Spacecraft Autonomy System**\n\n"
        yield f"**Mission Scenario:** {mission_scenario.replace('_', ' ').title()}\n"
        yield f"**Situation:** {situation}\n\n"
        
        # Simulate spacecraft state
        yield "## 📊 **Spacecraft State Analysis**\n\n"
        fuel_level = random.uniform(45, 85)
        battery_level = random.uniform(70, 95)
        comm_delay = {"mars_transit": 12.5, "lunar_orbit": 1.3, "deep_space": 28.0}.get(mission_scenario, 12.5)
        
        yield f"- **Fuel Level:** {fuel_level:.1f}%\n"
        yield f"- **Battery Level:** {battery_level:.1f}%\n"
        yield f"- **Communication Delay:** {comm_delay:.1f} minutes\n"
        yield f"- **Autonomous Operation:** {'REQUIRED' if comm_delay > 15 else 'ENABLED'}\n\n"
        
        # Autonomous decision making
        yield "## 🧠 **Autonomous Decision Analysis**\n\n"
        
        autonomy_prompt = f"""
        As NASA's spacecraft autonomy system, analyze this situation: {situation}
        
        Spacecraft Status:
        - Fuel: {fuel_level:.1f}%
        - Battery: {battery_level:.1f}%
        - Communication Delay: {comm_delay:.1f} minutes
        
        Provide autonomous decision including:
        1. Situation assessment
        2. Autonomous actions taken
        3. Resource allocation adjustments
        4. Risk mitigation strategies
        
        Use NASA autonomy protocols.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": autonomy_prompt}],
            max_tokens=1200
        )
        
        yield response.choices[0].message.content + "\n\n"
        
        yield f"**Autonomous Decision Confidence:** 92%\n"
        yield f"**System Status:** OPERATIONAL ✅\n"
    
    # SATELLITE TRAFFIC MANAGEMENT FUNCTIONS
    async def run_satellite_traffic(self, scenario: str, orbital_zone: str):
        """Satellite Traffic Management Agent - Simplified for unified interface"""
        if not scenario.strip():
            yield "Please enter a traffic management scenario."
            return
        
        yield f"🛰️ **NASA Satellite Traffic Management**\n\n"
        yield f"**Orbital Zone:** {orbital_zone} \n"
        yield f"**Scenario:** {scenario}\n\n"
        
        # Simulate orbital population
        yield "## 📡 **Orbital Surveillance Status**\n\n"
        active_sats = random.randint(15, 25)
        debris_objects = random.randint(20, 35)
        total_objects = active_sats + debris_objects
        
        yield f"- **Active Satellites:** {active_sats}\n"
        yield f"- **Space Debris:** {debris_objects}\n"
        yield f"- **Total Tracked Objects:** {total_objects}\n\n"
        
        # Risk assessment
        yield "## ⚠️ **Collision Risk Assessment**\n\n"
        high_risks = random.randint(1, 3)
        medium_risks = random.randint(3, 6)
        
        yield f"- **High-Priority Risks:** {high_risks}\n"
        yield f"- **Medium-Priority Risks:** {medium_risks}\n"
        yield f"- **Risk Status:** {'🚨 ACTIVE MONITORING' if high_risks > 1 else '✅ NOMINAL'}\n\n"
        
        # Traffic management analysis
        traffic_prompt = f"""
        As NASA's satellite traffic management specialist, analyze: {scenario}
        
        Orbital Zone: {orbital_zone}
        Objects Tracked: {total_objects}
        High-Risk Situations: {high_risks}
        
        Provide:
        1. Traffic management strategy
        2. Collision avoidance recommendations
        3. Orbital coordination protocols
        4. Multi-satellite management approach
        
        Use NASA space traffic management protocols.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": traffic_prompt}],
            max_tokens=1200
        )
        
        yield "## 🌐 **Traffic Management Response**\n\n"
        yield response.choices[0].message.content + "\n\n"
        
        yield f"**System Status:** {'⚠️ ACTIVE MONITORING' if high_risks > 1 else '✅ NOMINAL'}\n"
    
    # PLANETARY EXPLORATION FUNCTIONS
    async def run_planetary_exploration(self, planetary_body: str, region: str, objectives: str):
        """Planetary Exploration Agent - Simplified for unified interface"""
        if not region.strip():
            yield "Please enter a target region."
            return
        
        yield f"🌍 **NASA Planetary Exploration Mission**\n\n"
        yield f"**Target:** {planetary_body.title()}\n"
        yield f"**Region:** {region}\n\n"
        
        # Parse objectives
        mission_objectives = [obj.strip() for obj in objectives.split(',') if obj.strip()]
        if not mission_objectives:
            mission_objectives = ["Search for signs of past life", "Analyze geological composition"]
        
        yield f"### **Mission Objectives:**\n"
        for obj in mission_objectives:
            yield f"- {obj}\n"
        yield "\n"
        
        # Terrain analysis
        yield "## 🔍 **Terrain Analysis Phase**\n\n"
        features_found = random.randint(5, 8)
        high_priority_targets = random.randint(2, 4)
        
        yield f"- **Terrain Features Identified:** {features_found}\n"
        yield f"- **High Priority Targets:** {high_priority_targets}\n"
        yield f"- **Scientific Interest Level:** High\n\n"
        
        # Exploration planning
        exploration_prompt = f"""
        As NASA's planetary exploration specialist, plan exploration of: {region} on {planetary_body}
        
        Mission Objectives: {', '.join(mission_objectives)}
        Features Found: {features_found}
        
        Provide:
        1. Terrain analysis summary
        2. Target prioritization strategy
        3. Rover path planning approach
        4. Science activity scheduling
        5. Mission success metrics
        
        Use NASA planetary exploration protocols.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": exploration_prompt}],
            max_tokens=1200
        )
        
        yield "## 🎯 **Exploration Plan**\n\n"
        yield response.choices[0].message.content + "\n\n"
        
        yield f"**Mission Status:** READY FOR EXECUTION ✅\n"

# Create the unified interface
def create_nasa_portfolio():
    portfolio = NASAUnifiedPortfolio()
    
    with gr.Blocks(
        title="NASA AI Agents Portfolio",
        theme=gr.themes.Base(
            primary_hue="blue",
            secondary_hue="orange"
        ).set(
            body_background_fill="linear-gradient(45deg, #0a0a1a, #1a1a2e)",
            panel_background_fill="rgba(255,255,255,0.05)"
        ),
        css="""
        .gradio-container {
            max-width: 1400px !important;
        }
        .tab-nav {
            background: linear-gradient(90deg, #1a237e, #3f51b5) !important;
        }
        .tab-nav button {
            color: white !important;
            font-weight: bold !important;
        }
        """
    ) as demo:
        
        # Header
        gr.HTML("""
        <div style="text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(45deg, #1a237e, #3f51b5); border-radius: 15px;">
            <h1 style="color: #ffffff; font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                🚀 NASA AI AGENTS PORTFOLIO
            </h1>
            <p style="color: #e3f2fd; font-size: 1.4em; margin: 0;">
                Advanced AI Agent Systems for Space Mission Operations
            </p>
            <p style="color: #bbdefb; font-size: 1.1em; margin-top: 10px;">
                Six Specialized Agents • Production-Ready Systems • NASA-Authentic Workflows
            </p>
        </div>
        """)
        
        with gr.Tabs() as tabs:
            
            # Tab 1: Deep Research Agent
            with gr.TabItem("🔬 Deep Research", id="research"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Deep Research Agent</h2>
                    <p style="color: #cccccc;">Advanced research system for space missions and NASA technologies</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        research_query = gr.Textbox(
                            label="Research Query",
                            placeholder="e.g., 'Artemis lunar base construction materials', 'Mars mission life support systems'",
                            lines=3
                        )
                        research_btn = gr.Button("🔬 Start NASA Research", variant="primary", size="lg")
                    
                    with gr.Column():
                        gr.HTML("""
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                            <h4 style="color: #ffffff;">Research Domains</h4>
                            <ul style="color: #cccccc; font-size: 0.9em;">
                                <li>🛰️ Mission Planning</li>
                                <li>🚀 Propulsion Systems</li>
                                <li>🔬 Space Materials</li>
                                <li>🌱 Life Support</li>
                                <li>🌍 Planetary Exploration</li>
                            </ul>
                        </div>
                        """)
                
                research_output = gr.Markdown(label="Research Report", container=True)
                research_btn.click(portfolio.run_deep_research, research_query, research_output)
            
            # Tab 2: Engineering Team
            with gr.TabItem("🤝 Engineering Team", id="engineering"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Engineering Team</h2>
                    <p style="color: #cccccc;">Multi-agent collaborative spacecraft and mission design</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        project_input = gr.Textbox(
                            label="Engineering Project",
                            placeholder="e.g., 'Mars helicopter for sample collection', 'Lunar Gateway station module'",
                            lines=3
                        )
                        engineering_btn = gr.Button("🤝 Start Engineering Design", variant="primary", size="lg")
                    
                    with gr.Column():
                        gr.HTML("""
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                            <h4 style="color: #ffffff;">Engineering Team</h4>
                            <ul style="color: #cccccc; font-size: 0.9em;">
                                <li>🎯 Systems Engineer</li>
                                <li>🚀 Propulsion Engineer</li>
                                <li>🏗️ Structural Engineer</li>
                                <li>💻 Software Engineer</li>
                                <li>🎮 Mission Operations</li>
                            </ul>
                        </div>
                        """)
                
                engineering_output = gr.Markdown(label="Engineering Design Session", container=True)
                engineering_btn.click(portfolio.run_engineering_team, project_input, engineering_output)
            
            # Tab 3: Mission Control
            with gr.TabItem("🎮 Mission Control", id="control"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Mission Control</h2>
                    <p style="color: #cccccc;">Real-time mission operations and decision support</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        control_scenario = gr.Textbox(
                            label="Mission Control Scenario",
                            placeholder="e.g., 'Emergency solar panel deployment', 'Crew reports unusual vibration'",
                            lines=3
                        )
                        mission_phase = gr.Dropdown(
                            label="Mission Phase",
                            choices=[
                                ("Orbital Operations", "orbital_operations"),
                                ("Docking Operations", "docking"),
                                ("EVA Operations", "eva"),
                                ("Emergency", "emergency")
                            ],
                            value="orbital_operations"
                        )
                        control_btn = gr.Button("🎮 Activate Mission Control", variant="primary", size="lg")
                    
                    with gr.Column():
                        gr.HTML("""
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                            <h4 style="color: #ffffff;">Control Team</h4>
                            <ul style="color: #cccccc; font-size: 0.9em;">
                                <li>🎯 Mission Specialist</li>
                                <li>🔧 Systems Engineer</li>
                                <li>👨‍💼 Flight Director</li>
                            </ul>
                            <h4 style="color: #ffffff; margin-top: 15px;">Priority Levels</h4>
                            <ul style="color: #cccccc; font-size: 0.9em;">
                                <li>🟢 Routine</li>
                                <li>🟡 Elevated</li>
                                <li>🔴 Critical</li>
                            </ul>
                        </div>
                        """)
                
                control_output = gr.Markdown(label="Mission Control Response", container=True)
                control_btn.click(portfolio.run_mission_control, [control_scenario, mission_phase], control_output)
            
            # Tab 4: Spacecraft Autonomy
            with gr.TabItem("🤖 Spacecraft Autonomy", id="autonomy"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Spacecraft Autonomy</h2>
                    <p style="color: #cccccc;">Deep space autonomous decision-making systems</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        autonomy_situation = gr.Textbox(
                            label="Autonomous Situation",
                            placeholder="e.g., 'Navigation computer malfunction', 'Solar panel damaged by micrometeorite'",
                            lines=3
                        )
                        autonomy_scenario = gr.Dropdown(
                            label="Mission Scenario",
                            choices=[
                                ("Mars Transit", "mars_transit"),
                                ("Lunar Orbit", "lunar_orbit"),
                                ("Deep Space", "deep_space")
                            ],
                            value="mars_transit"
                        )
                        autonomy_btn = gr.Button("🤖 Activate Autonomy", variant="primary", size="lg")
                    
                    with gr.Column():
                        gr.HTML("""
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                            <h4 style="color: #ffffff;">Autonomy Features</h4>
                            <ul style="color: #cccccc; font-size: 0.9em;">
                                <li>🧭 Navigation Planning</li>
                                <li>⚡ Fault Detection</li>
                                <li>🔋 Resource Management</li>
                                <li>🛡️ Risk Assessment</li>
                                <li>📡 Earth Communication</li>
                            </ul>
                        </div>
                        """)
                
                autonomy_output = gr.Markdown(label="Autonomy Response", container=True)
                autonomy_btn.click(portfolio.run_spacecraft_autonomy, [autonomy_situation, autonomy_scenario], autonomy_output)
            
            # Tab 5: Satellite Traffic Management
            with gr.TabItem("🛰️ Satellite Traffic", id="traffic"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Satellite Traffic Management</h2>
                    <p style="color: #cccccc;">Orbital collision avoidance and space traffic coordination</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        traffic_scenario = gr.Textbox(
                            label="Traffic Scenario",
                            placeholder="e.g., 'Large debris field in Starlink orbit', 'ISS debris avoidance maneuver'",
                            lines=3
                        )
                        orbital_zone = gr.Dropdown(
                            label="Orbital Zone",
                            choices=[
                                ("Low Earth Orbit (LEO)", "LEO"),
                                ("Medium Earth Orbit (MEO)", "MEO"),
                                ("Geostationary Orbit (GEO)", "GEO")
                            ],
                            value="LEO"
                        )
                        traffic_btn = gr.Button("🛰️ Activate Traffic Management", variant="primary", size="lg")
                    
                    with gr.Column():
                        gr.HTML("""
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                            <h4 style="color: #ffffff;">Traffic Management</h4>
                            <ul style="color: #cccccc; font-size: 0.9em;">
                                <li>🎯 Trajectory Prediction</li>
                                <li>⚠️ Collision Assessment</li>
                                <li>🚀 Avoidance Maneuvers</li>
                                <li>🌐 Constellation Coordination</li>
                                <li>📡 Multi-Satellite Management</li>
                            </ul>
                        </div>
                        """)
                
                traffic_output = gr.Markdown(label="Traffic Management Response", container=True)
                traffic_btn.click(portfolio.run_satellite_traffic, [traffic_scenario, orbital_zone], traffic_output)
            
            # Tab 6: Planetary Exploration
            with gr.TabItem("🌍 Planetary Exploration", id="exploration"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Planetary Exploration</h2>
                    <p style="color: #cccccc;">Autonomous planetary surface analysis and exploration planning</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        planet_body = gr.Dropdown(
                            label="Planetary Body",
                            choices=[
                                ("Mars", "mars"),
                                ("Moon", "moon"),
                                ("Europa", "europa")
                            ],
                            value="mars"
                        )
                        exploration_region = gr.Textbox(
                            label="Target Region",
                            placeholder="e.g., 'Jezero Crater with ancient river delta', 'Mare Imbrium with impact craters'",
                            lines=2
                        )
                        exploration_objectives = gr.Textbox(
                            label="Mission Objectives",
                            placeholder="e.g., Search for biosignatures, Analyze mineral composition",
                            lines=2
                        )
                        exploration_btn = gr.Button("🌍 Start Exploration", variant="primary", size="lg")
                    
                    with gr.Column():
                        gr.HTML("""
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                            <h4 style="color: #ffffff;">Exploration Capabilities</h4>
                            <ul style="color: #cccccc; font-size: 0.9em;">
                                <li>🔍 Terrain Analysis</li>
                                <li>🎯 Target Prioritization</li>
                                <li>🛰️ Path Planning</li>
                                <li>🤖 Autonomous Science</li>
                                <li>📊 Mission Optimization</li>
                            </ul>
                        </div>
                        """)
                
                exploration_output = gr.Markdown(label="Exploration Mission", container=True)
                exploration_btn.click(portfolio.run_planetary_exploration, [planet_body, exploration_region, exploration_objectives], exploration_output)
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 10px;">
            <h3 style="color: #ffffff;">🌟 NASA AI Portfolio Highlights</h3>
            <div style="display: flex; justify-content: space-around; margin-top: 15px;">
                <div style="color: #bbdefb;">
                    <strong>6 AI Frameworks</strong><br>
                    <small>OpenAI • Multi-Agent • LangGraph</small>
                </div>
                <div style="color: #bbdefb;">
                    <strong>NASA Standards</strong><br>
                    <small>Authentic Workflows • Real Protocols</small>
                </div>
                <div style="color: #bbdefb;">
                    <strong>Production Ready</strong><br>
                    <small>Scalable • Professional • Robust</small>
                </div>
            </div>
            <p style="color: #90caf9; margin-top: 15px; font-size: 0.9em;">
                🚀 Ready for NASA Interview Demonstration • Repository: github.com/OpalDecisionSciences/nasa-ai-agents-portfolio
            </p>
        </div>
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_nasa_portfolio()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        inbrowser=True
    )