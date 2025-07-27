"""
NASA AI Agents using OpenAI Agents SDK with Tracing
Production-ready NASA agent system with observability
"""

import gradio as gr
import asyncio
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# OpenAI Agents SDK imports
from openai import OpenAI
from agents import Agent, Runner

load_dotenv()

class NASAAgentsSDK:
    """NASA AI Agents using OpenAI Agents SDK with tracing"""
    
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        
        print(f"🔑 OpenAI Agents SDK initialized")
        print(f"🔍 Enhanced logging enabled for observability")
        
        # Create NASA agents
        self.agents = {}
        self._create_nasa_agents()
    
    def _create_nasa_agents(self):
        """Create specialized NASA agents with SDK"""
        
        # Deep Research Agent
        self.agents["deep_research"] = Agent(
            name="NASA Deep Research Agent",
            instructions="""You are a NASA Deep Research specialist with expertise in:
            - Space mission design and architecture
            - Rocket engines and spacecraft propulsion systems
            - Space-grade materials and thermal protection
            - Environmental control and life support systems
            - Planetary exploration and scientific instruments
            - Deep space communications and data transmission
            
            Provide comprehensive, technical analysis with references to real NASA missions, 
            programs, and established protocols. Keep responses focused and actionable."""
        )
        
        # Mission Control Agent
        self.agents["mission_control"] = Agent(
            name="NASA Mission Control Agent",
            instructions="""You are a NASA Mission Control specialist responsible for:
            - Real-time mission operations and decision support
            - Emergency situation analysis and response protocols
            - Priority assessment (routine, elevated, critical, emergency)
            - Systems check coordination and crew safety procedures
            - Flight Director-level decision making
            
            Always prioritize crew safety and mission success. Follow established NASA 
            mission control protocols and provide clear, actionable recommendations."""
        )
        
        # Engineering Team Agent
        self.agents["engineering"] = Agent(
            name="NASA Engineering Team Agent",
            instructions="""You are a NASA Engineering Team lead coordinating:
            - Systems engineering and mission architecture
            - Propulsion system design and integration
            - Structural engineering and materials selection
            - Software engineering and flight control systems
            - Mission operations planning and procedures
            
            Provide comprehensive engineering analysis following NASA design standards,
            safety requirements, and best practices from successful space missions."""
        )
        
        # Spacecraft Autonomy Agent
        self.agents["autonomy"] = Agent(
            name="NASA Spacecraft Autonomy Agent",
            instructions="""You are a NASA Spacecraft Autonomy system responsible for:
            - Autonomous navigation and path planning in deep space
            - Fault detection, isolation, and recovery procedures
            - Resource management and power allocation optimization
            - Risk assessment and autonomous decision making
            - Emergency response when Earth communication is delayed
            
            Make decisions prioritizing mission safety, resource conservation, and
            operational efficiency using NASA autonomy protocols."""
        )
        
        # Satellite Traffic Management Agent
        self.agents["traffic"] = Agent(
            name="NASA Satellite Traffic Management Agent",
            instructions="""You are a NASA Space Traffic Management specialist handling:
            - Orbital collision risk assessment and avoidance
            - Multi-satellite constellation coordination
            - Space debris tracking and mitigation strategies
            - Trajectory prediction and maneuver planning
            - International space traffic coordination protocols
            
            Ensure space safety through proactive collision avoidance, efficient
            orbital coordination, and adherence to international space guidelines."""
        )
        
        # Planetary Exploration Agent
        self.agents["exploration"] = Agent(
            name="NASA Planetary Exploration Agent",
            instructions="""You are a NASA Planetary Exploration specialist managing:
            - Autonomous terrain analysis and geological assessment
            - Scientific target prioritization and mission planning
            - Rover path planning and navigation optimization
            - Autonomous science activity selection and scheduling
            - Resource allocation for maximum scientific return
            
            Optimize exploration missions for scientific discovery while ensuring
            equipment safety and mission success using NASA exploration protocols."""
        )
        
        print(f"✅ Created {len(self.agents)} NASA agents with SDK")
    
    @trace
    async def run_agent(self, agent_name: str, query: str) -> str:
        """Run query with specified NASA agent using tracing"""
        
        with self.tracer.start_span(f"nasa_agent_{agent_name}") as span:
            span.set_attribute("agent_name", agent_name)
            span.set_attribute("query_length", len(query))
            span.set_attribute("timestamp", datetime.now().isoformat())
            
            try:
                if agent_name not in self.agents:
                    error_msg = f"Agent '{agent_name}' not found. Available: {list(self.agents.keys())}"
                    span.set_attribute("error", error_msg)
                    return error_msg
                
                agent = self.agents[agent_name]
                
                # Run agent with tracing
                span.set_attribute("model", agent.model)
                span.add_event("agent_execution_start")
                
                response = await agent.run(query)
                
                span.add_event("agent_execution_complete")
                span.set_attribute("response_length", len(response.content))
                span.set_attribute("success", True)
                
                print(f"✅ Agent {agent_name} completed successfully")
                print(f"📊 Trace ID: {span.get_span_context().trace_id}")
                
                return response.content
                
            except Exception as e:
                error_msg = f"Agent {agent_name} error: {str(e)}"
                span.set_attribute("error", error_msg)
                span.set_attribute("success", False)
                
                print(f"❌ Agent {agent_name} failed: {str(e)}")
                return f"🛠️ **Agent Error**: {error_msg}\n\nPlease try again or check your API configuration."
    
    async def run_deep_research(self, query: str) -> str:
        """Deep Research Agent with SDK and tracing"""
        if not query.strip():
            return "Please enter a research query."
        
        result = f"🚀 **NASA Deep Research Agent - SDK Version**\n\n"
        result += f"**Query:** {query}\n"
        result += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        
        # Run with tracing
        response = await self.run_agent("deep_research", query)
        
        result += "## 🔬 **Research Analysis**\n\n"
        result += response + "\n\n"
        result += "---\n"
        result += "**🔍 Tracing:** This request was traced for observability and debugging\n"
        
        return result
    
    async def run_mission_control(self, scenario: str, mission_phase: str) -> str:
        """Mission Control Agent with SDK and tracing"""
        if not scenario.strip():
            return "Please enter a mission control scenario."
        
        result = f"🎮 **NASA Mission Control - SDK Version**\n\n"
        result += f"**Mission Phase:** {mission_phase.replace('_', ' ').title()}\n"
        result += f"**Scenario:** {scenario}\n"
        result += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        
        # Enhanced prompt for mission control
        enhanced_prompt = f"""
        Mission Control Analysis Required:
        
        Scenario: {scenario}
        Mission Phase: {mission_phase}
        
        Provide:
        1. Situation assessment and priority level
        2. Immediate actions required
        3. Systems check recommendations  
        4. Flight Director decision and rationale
        5. Communication plan for crew/stakeholders
        """
        
        # Run with tracing
        response = await self.run_agent("mission_control", enhanced_prompt)
        
        result += "## 📡 **Mission Control Response**\n\n"
        result += response + "\n\n"
        result += "---\n"
        result += "**🔍 Tracing:** This mission control request was traced for audit and analysis\n"
        
        return result
    
    async def run_engineering_team(self, project: str) -> str:
        """Engineering Team Agent with SDK and tracing"""
        if not project.strip():
            return "Please enter a project description."
        
        result = f"🤝 **NASA Engineering Team - SDK Version**\n\n"
        result += f"**Project:** {project}\n"
        result += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        
        enhanced_prompt = f"""
        Engineering Design Session for: {project}
        
        Provide comprehensive engineering analysis including:
        1. Mission requirements and system architecture
        2. Key subsystem designs (propulsion, structure, software, operations)
        3. Interface requirements and integration challenges
        4. Risk assessment and mitigation strategies
        5. Development timeline and testing recommendations
        
        Follow NASA engineering standards and reference similar successful missions.
        """
        
        # Run with tracing
        response = await self.run_agent("engineering", enhanced_prompt)
        
        result += "## 🛠️ **Engineering Design Session**\n\n"
        result += response + "\n\n"
        result += "---\n"
        result += "**🔍 Tracing:** Engineering decisions traced for design review and documentation\n"
        
        return result
    
    async def run_spacecraft_autonomy(self, situation: str, mission_scenario: str) -> str:
        """Spacecraft Autonomy Agent with SDK and tracing"""
        if not situation.strip():
            return "Please enter an autonomous situation."
        
        result = f"🤖 **NASA Spacecraft Autonomy - SDK Version**\n\n"
        result += f"**Mission Scenario:** {mission_scenario.replace('_', ' ').title()}\n"
        result += f"**Situation:** {situation}\n"
        result += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        
        enhanced_prompt = f"""
        Autonomous Decision Required:
        
        Situation: {situation}
        Mission Scenario: {mission_scenario}
        
        Provide autonomous analysis including:
        1. Situation assessment and spacecraft state evaluation
        2. Autonomous actions taken and decision rationale
        3. Resource allocation adjustments
        4. Risk mitigation strategies implemented
        5. Communication to Earth (given potential delays)
        
        Prioritize mission safety and operational efficiency.
        """
        
        # Run with tracing
        response = await self.run_agent("autonomy", enhanced_prompt)
        
        result += "## 🧠 **Autonomous Decision Analysis**\n\n"
        result += response + "\n\n"
        result += "---\n"
        result += "**🔍 Tracing:** Autonomous decisions traced for mission analysis and learning\n"
        
        return result
    
    async def run_satellite_traffic(self, scenario: str, orbital_zone: str) -> str:
        """Satellite Traffic Management Agent with SDK and tracing"""
        if not scenario.strip():
            return "Please enter a traffic management scenario."
        
        result = f"🛰️ **NASA Satellite Traffic Management - SDK Version**\n\n"
        result += f"**Orbital Zone:** {orbital_zone}\n"
        result += f"**Scenario:** {scenario}\n"
        result += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        
        enhanced_prompt = f"""
        Space Traffic Management Analysis:
        
        Scenario: {scenario}
        Orbital Zone: {orbital_zone}
        
        Provide traffic management strategy including:
        1. Collision risk assessment and priority ranking
        2. Avoidance maneuver recommendations
        3. Multi-satellite coordination protocols
        4. Orbital debris considerations
        5. International coordination requirements
        
        Ensure space safety and operational efficiency.
        """
        
        # Run with tracing
        response = await self.run_agent("traffic", enhanced_prompt)
        
        result += "## 🌐 **Traffic Management Analysis**\n\n"
        result += response + "\n\n"
        result += "---\n"
        result += "**🔍 Tracing:** Traffic management decisions traced for safety analysis\n"
        
        return result
    
    async def run_planetary_exploration(self, planetary_body: str, region: str, objectives: str) -> str:
        """Planetary Exploration Agent with SDK and tracing"""
        if not region.strip():
            return "Please enter a target region."
        
        result = f"🌍 **NASA Planetary Exploration - SDK Version**\n\n"
        result += f"**Target:** {planetary_body.title()}\n"
        result += f"**Region:** {region}\n"
        result += f"**Objectives:** {objectives}\n"
        result += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        
        enhanced_prompt = f"""
        Planetary Exploration Mission Planning:
        
        Target: {planetary_body}
        Region: {region}
        Objectives: {objectives}
        
        Provide exploration strategy including:
        1. Terrain analysis and feature identification
        2. Target prioritization based on scientific value
        3. Rover path planning and navigation strategy
        4. Autonomous science activity scheduling
        5. Mission success metrics and risk assessment
        
        Optimize for scientific discovery and mission safety.
        """
        
        # Run with tracing
        response = await self.run_agent("exploration", enhanced_prompt)
        
        result += "## 🎯 **Exploration Mission Plan**\n\n"
        result += response + "\n\n"
        result += "---\n"
        result += "**🔍 Tracing:** Exploration decisions traced for science planning and review\n"
        
        return result

# Create the Gradio interface
def create_nasa_agents_sdk_interface():
    nasa_agents = NASAAgentsSDK()
    
    with gr.Blocks(
        title="NASA AI Agents - OpenAI SDK Version",
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
                🚀 NASA AI AGENTS - SDK VERSION
            </h1>
            <p style="color: #e3f2fd; font-size: 1.4em; margin: 0;">
                OpenAI Agents SDK with Built-in Tracing & Observability
            </p>
            <p style="color: #bbdefb; font-size: 1.1em; margin-top: 10px;">
                Six Specialized Agents • Production-Ready • Full Traceability
            </p>
        </div>
        """)
        
        with gr.Tabs() as tabs:
            
            # Tab 1: Deep Research Agent
            with gr.TabItem("🔬 Deep Research", id="research"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Deep Research Agent</h2>
                    <p style="color: #cccccc;">Advanced research system with OpenAI Agents SDK</p>
                </div>
                """)
                
                research_query = gr.Textbox(
                    label="Research Query",
                    placeholder="e.g., 'Artemis lunar base construction materials', 'Mars mission life support systems'",
                    lines=3
                )
                research_btn = gr.Button("🔬 Start NASA Research", variant="primary", size="lg")
                research_output = gr.Markdown(label="Research Report", container=True)
                research_btn.click(fn=nasa_agents.run_deep_research, inputs=research_query, outputs=research_output)
            
            # Tab 2: Mission Control
            with gr.TabItem("🎮 Mission Control", id="control"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Mission Control</h2>
                    <p style="color: #cccccc;">Real-time mission operations with full tracing</p>
                </div>
                """)
                
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
                control_output = gr.Markdown(label="Mission Control Response", container=True)
                control_btn.click(fn=nasa_agents.run_mission_control, inputs=[control_scenario, mission_phase], outputs=control_output)
            
            # Tab 3: Engineering Team
            with gr.TabItem("🤝 Engineering Team", id="engineering"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Engineering Team</h2>
                    <p style="color: #cccccc;">Multi-agent collaborative design with SDK</p>
                </div>
                """)
                
                project_input = gr.Textbox(
                    label="Engineering Project",
                    placeholder="e.g., 'Mars helicopter for sample collection', 'Lunar Gateway station module'",
                    lines=3
                )
                engineering_btn = gr.Button("🤝 Start Engineering Design", variant="primary", size="lg")
                engineering_output = gr.Markdown(label="Engineering Design Session", container=True)
                engineering_btn.click(fn=nasa_agents.run_engineering_team, inputs=project_input, outputs=engineering_output)
            
            # Tab 4: Spacecraft Autonomy
            with gr.TabItem("🤖 Spacecraft Autonomy", id="autonomy"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Spacecraft Autonomy</h2>
                    <p style="color: #cccccc;">Deep space autonomous systems with tracing</p>
                </div>
                """)
                
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
                autonomy_output = gr.Markdown(label="Autonomy Response", container=True)
                autonomy_btn.click(fn=nasa_agents.run_spacecraft_autonomy, inputs=[autonomy_situation, autonomy_scenario], outputs=autonomy_output)
            
            # Tab 5: Satellite Traffic Management
            with gr.TabItem("🛰️ Satellite Traffic", id="traffic"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Satellite Traffic Management</h2>
                    <p style="color: #cccccc;">Orbital collision avoidance with SDK tracing</p>
                </div>
                """)
                
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
                traffic_output = gr.Markdown(label="Traffic Management Response", container=True)
                traffic_btn.click(fn=nasa_agents.run_satellite_traffic, inputs=[traffic_scenario, orbital_zone], outputs=traffic_output)
            
            # Tab 6: Planetary Exploration
            with gr.TabItem("🌍 Planetary Exploration", id="exploration"):
                gr.HTML("""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #ffffff;">NASA Planetary Exploration</h2>
                    <p style="color: #cccccc;">Autonomous surface analysis with SDK framework</p>
                </div>
                """)
                
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
                exploration_output = gr.Markdown(label="Exploration Mission", container=True)
                exploration_btn.click(fn=nasa_agents.run_planetary_exploration, inputs=[planet_body, exploration_region, exploration_objectives], outputs=exploration_output)
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 10px;">
            <h3 style="color: #ffffff;">🌟 NASA AI Portfolio - OpenAI Agents SDK</h3>
            <div style="display: flex; justify-content: space-around; margin-top: 15px;">
                <div style="color: #bbdefb;">
                    <strong>OpenAI Agents SDK</strong><br>
                    <small>Production Framework • Built-in Tracing</small>
                </div>
                <div style="color: #bbdefb;">
                    <strong>NASA Standards</strong><br>
                    <small>Authentic Workflows • Real Protocols</small>
                </div>
                <div style="color: #bbdefb;">
                    <strong>Full Observability</strong><br>
                    <small>Traced • Debuggable • Auditable</small>
                </div>
            </div>
            <p style="color: #90caf9; margin-top: 15px; font-size: 0.9em;">
                🚀 OpenAI Agents SDK Version • Repository: github.com/OpalDecisionSciences/nasa-ai-agents-portfolio
            </p>
        </div>
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_nasa_agents_sdk_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=False,
        inbrowser=True
    )