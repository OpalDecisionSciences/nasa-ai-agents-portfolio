"""
NASA Mission Control Sidekick
Advanced LangGraph-based agent for mission operations, real-time decision making, and emergency response
"""

from typing import Annotated, List, Any, Optional, Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field
import uuid
import asyncio
import os
from datetime import datetime
import gradio as gr
import json
from dotenv import load_dotenv

load_dotenv()

# Mission Control State
class MissionState(TypedDict):
    messages: Annotated[List[Any], add_messages]
    mission_phase: str
    priority_level: str
    systems_status: Dict[str, str]
    crew_status: str
    mission_objectives: List[str]
    emergency_procedures: bool
    flight_director_approval: bool

# Analysis Output Models
class MissionAnalysis(BaseModel):
    situation_assessment: str = Field(description="Current mission situation analysis")
    priority_level: str = Field(description="Priority level: routine, elevated, critical, emergency")
    recommended_actions: List[str] = Field(description="Recommended immediate actions")
    systems_check_required: bool = Field(description="Whether systems check is needed")
    crew_notification_required: bool = Field(description="Whether crew notification is needed")
    flight_director_escalation: bool = Field(description="Whether Flight Director escalation is required")

class SystemsCheck(BaseModel):
    primary_systems: Dict[str, str] = Field(description="Status of primary spacecraft systems")
    backup_systems: Dict[str, str] = Field(description="Status of backup systems")
    life_support: str = Field(description="Life support systems status")
    communications: str = Field(description="Communications systems status")
    navigation: str = Field(description="Navigation and guidance status")
    overall_health: str = Field(description="Overall spacecraft health assessment")

# NASA Mission Control Tools
async def get_telemetry_data() -> str:
    """Simulate getting real-time telemetry data"""
    await asyncio.sleep(1)  # Simulate data retrieval delay
    
    telemetry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "altitude": "408.5 km",
        "velocity": "7.66 km/s",
        "orbital_position": "32.5°N, 85.2°W",
        "power_level": "94%",
        "communication_signal": "Strong",
        "crew_vitals": "Nominal",
        "experiments_status": "Active - 3/5 running"
    }
    
    return json.dumps(telemetry, indent=2)

async def check_mission_timeline() -> str:
    """Check current mission timeline and upcoming activities"""
    await asyncio.sleep(1)
    
    timeline = {
        "current_time": datetime.now().strftime("%H:%M UTC"),
        "current_activity": "Scientific observations - Earth imaging",
        "next_activity": "Crew exercise period (T+45 min)",
        "upcoming_critical_events": [
            "Docking procedure - T+6 hours",
            "EVA preparation - T+18 hours",
            "Orbital adjustment burn - T+24 hours"
        ],
        "mission_day": "Mission Day 15",
        "days_remaining": "195 days"
    }
    
    return json.dumps(timeline, indent=2)

async def emergency_protocols() -> str:
    """Access emergency protocols and procedures"""
    await asyncio.sleep(1)
    
    protocols = {
        "active_procedures": "Emergency Response Checklist v2.1",
        "immediate_actions": [
            "Secure crew safety",
            "Assess system damage",
            "Establish communication with Mission Control",
            "Implement contingency procedures"
        ],
        "communication_priorities": [
            "Life support systems",
            "Structural integrity", 
            "Navigation and control",
            "Power and thermal systems"
        ],
        "backup_options": [
            "Alternative power sources",
            "Backup communication channels",
            "Emergency return procedures",
            "Crew evacuation protocols"
        ]
    }
    
    return json.dumps(protocols, indent=2)

# NASA Mission Control Agent
class NASAMissionControl:
    def __init__(self):
        self.mission_specialist_llm = None
        self.flight_director_llm = None
        self.systems_engineer_llm = None
        self.tools = []
        self.graph = None
        self.session_id = str(uuid.uuid4())
        self.memory = MemorySaver()
        
        # NASA mission phases
        self.mission_phases = {
            "pre_launch": "Pre-launch preparation and final checks",
            "launch": "Launch and ascent to orbit",
            "orbital_operations": "On-orbit operations and experiments",
            "docking": "Docking or rendezvous operations",
            "eva": "Extravehicular activity operations",
            "return": "Return and landing preparation",
            "emergency": "Emergency or contingency operations"
        }
    
    async def setup(self):
        """Initialize the mission control system"""
        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # Initialize LLMs for different roles
        self.mission_specialist_llm = ChatOpenAI(model=model, temperature=0.1, api_key=api_key)
        self.flight_director_llm = ChatOpenAI(model=model, temperature=0.0, api_key=api_key)  # Most conservative
        self.systems_engineer_llm = ChatOpenAI(model=model, temperature=0.1, api_key=api_key)
        
        # Setup tools (simplified for demo)
        self.tools = []  # Tools would be added here in real implementation
        
        await self.build_graph()
    
    def mission_specialist(self, state: MissionState) -> Dict[str, Any]:
        """Mission Specialist - Initial assessment and analysis"""
        
        system_message = f"""
        You are a NASA Mission Specialist in Mission Control. Your role is to:
        
        1. Analyze incoming situations and requests
        2. Assess priority levels and urgency
        3. Recommend immediate actions
        4. Determine if systems checks or escalation are needed
        
        Current Mission Context:
        - Phase: {state.get('mission_phase', 'orbital_operations')}
        - Systems Status: {state.get('systems_status', {})}
        - Crew Status: {state.get('crew_status', 'nominal')}
        
        You must always prioritize crew safety and mission success. Use NASA protocols and procedures.
        Respond with a structured analysis including situation assessment, priority level, and recommended actions.
        """
        
        # Get the latest message
        latest_message = state["messages"][-1].content
        
        # Create analysis prompt
        analysis_prompt = f"""
        Analyze this mission control situation: {latest_message}
        
        Provide:
        1. Situation assessment
        2. Priority level (routine/elevated/critical/emergency)
        3. Recommended immediate actions
        4. Whether systems check is required
        5. Whether crew notification is required  
        6. Whether Flight Director escalation is required
        
        Consider NASA mission control protocols and crew safety as top priority.
        """
        
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=analysis_prompt)
        ]
        
        # Get structured output
        llm_with_output = self.mission_specialist_llm.with_structured_output(MissionAnalysis)
        analysis = llm_with_output.invoke(messages)
        
        # Update state
        new_state = {
            "messages": [AIMessage(content=f"Mission Specialist Analysis: {analysis.situation_assessment}")],
            "priority_level": analysis.priority_level,
            "emergency_procedures": analysis.priority_level in ["critical", "emergency"],
        }
        
        return new_state
    
    def systems_engineer(self, state: MissionState) -> Dict[str, Any]:
        """Systems Engineer - Technical systems analysis"""
        
        system_message = f"""
        You are a NASA Systems Engineer in Mission Control. Your role is to:
        
        1. Assess spacecraft and mission systems status
        2. Identify potential technical issues
        3. Recommend technical solutions and workarounds
        4. Ensure all systems are operating within parameters
        
        Current Priority Level: {state.get('priority_level', 'routine')}
        Emergency Procedures Active: {state.get('emergency_procedures', False)}
        """
        
        latest_message = state["messages"][-1].content
        
        systems_prompt = f"""
        Conduct a systems engineering analysis for: {latest_message}
        
        Assess and report on:
        1. Primary spacecraft systems (propulsion, power, thermal, etc.)
        2. Backup systems status
        3. Life support systems
        4. Communications systems
        5. Navigation and guidance systems
        6. Overall spacecraft health assessment
        
        Use NASA systems engineering protocols and provide technical recommendations.
        """
        
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=systems_prompt)
        ]
        
        llm_with_output = self.systems_engineer_llm.with_structured_output(SystemsCheck)
        systems_analysis = llm_with_output.invoke(messages)
        
        new_state = {
            "messages": [AIMessage(content=f"Systems Engineering Analysis: Overall spacecraft health is {systems_analysis.overall_health}")],
            "systems_status": systems_analysis.primary_systems
        }
        
        return new_state
    
    def flight_director(self, state: MissionState) -> Dict[str, Any]:
        """Flight Director - Final decision and authorization"""
        
        system_message = f"""
        You are a NASA Flight Director - the ultimate authority for this mission. Your responsibilities:
        
        1. Make final decisions on all mission operations
        2. Authorize critical procedures and actions
        3. Ensure crew safety above all else
        4. Coordinate between all mission control teams
        5. Communicate final decisions and rationale
        
        Priority Level: {state.get('priority_level', 'routine')}
        Emergency Status: {state.get('emergency_procedures', False)}
        Systems Status: {state.get('systems_status', {})}
        """
        
        # Gather all previous analysis
        conversation = "\n".join([msg.content for msg in state["messages"][-3:]])
        
        decision_prompt = f"""
        As Flight Director, review the mission control team analysis and make your final decision:
        
        {conversation}
        
        Provide:
        1. Your final decision and authorization
        2. Clear rationale for the decision
        3. Specific instructions for implementation
        4. Any additional safety measures required
        5. Communication plan for crew and stakeholders
        
        Remember: Crew safety is paramount. Mission success is secondary.
        """
        
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=decision_prompt)
        ]
        
        response = self.flight_director_llm.invoke(messages)
        
        new_state = {
            "messages": [AIMessage(content=f"Flight Director Decision: {response.content}")],
            "flight_director_approval": True
        }
        
        return new_state
    
    def route_analysis(self, state: MissionState) -> str:
        """Route based on priority level and analysis needs"""
        priority = state.get("priority_level", "routine")
        
        if priority in ["critical", "emergency"]:
            return "systems_engineer"
        elif priority == "elevated":
            return "systems_engineer"
        else:
            return "flight_director"
    
    def route_to_director(self, state: MissionState) -> str:
        """Route to flight director for final decision"""
        return "flight_director"
    
    def check_completion(self, state: MissionState) -> str:
        """Check if mission control process is complete"""
        if state.get("flight_director_approval", False):
            return "END"
        else:
            return "mission_specialist"
    
    async def build_graph(self):
        """Build the mission control workflow graph"""
        graph_builder = StateGraph(MissionState)
        
        # Add nodes
        graph_builder.add_node("mission_specialist", self.mission_specialist)
        graph_builder.add_node("systems_engineer", self.systems_engineer)
        graph_builder.add_node("flight_director", self.flight_director)
        
        # Add edges
        graph_builder.add_edge(START, "mission_specialist")
        graph_builder.add_conditional_edges(
            "mission_specialist", 
            self.route_analysis, 
            {"systems_engineer": "systems_engineer", "flight_director": "flight_director"}
        )
        graph_builder.add_edge("systems_engineer", "flight_director")
        graph_builder.add_edge("flight_director", END)
        
        # Compile graph
        self.graph = graph_builder.compile(checkpointer=self.memory)
    
    async def process_mission_request(self, request: str, mission_phase: str = "orbital_operations"):
        """Process a mission control request"""
        config = {"configurable": {"thread_id": self.session_id}}
        
        initial_state = {
            "messages": [HumanMessage(content=request)],
            "mission_phase": mission_phase,
            "priority_level": "routine",
            "systems_status": {},
            "crew_status": "nominal",
            "mission_objectives": [],
            "emergency_procedures": False,
            "flight_director_approval": False
        }
        
        result = await self.graph.ainvoke(initial_state, config=config)
        
        # Format response
        responses = []
        for msg in result["messages"]:
            if hasattr(msg, 'content'):
                responses.append(msg.content)
        
        return {
            "analysis": responses,
            "priority_level": result.get("priority_level", "routine"),
            "emergency_status": result.get("emergency_procedures", False),
            "systems_status": result.get("systems_status", {}),
            "approved": result.get("flight_director_approval", False)
        }

# Gradio Interface Functions
async def process_mission_control_request(request: str, mission_phase: str):
    """Process mission control request and return formatted response"""
    
    # Initialize mission control
    mission_control = NASAMissionControl()
    await mission_control.setup()
    
    # Process the request
    result = await mission_control.process_mission_request(request, mission_phase)
    
    # Format output
    output = f"# 🚀 NASA Mission Control Response\n\n"
    output += f"**Mission Phase:** {mission_phase.replace('_', ' ').title()}\n"
    output += f"**Priority Level:** {result['priority_level'].upper()}\n"
    output += f"**Emergency Status:** {'🚨 ACTIVE' if result['emergency_status'] else '✅ Normal'}\n"
    output += f"**Flight Director Approval:** {'✅ Authorized' if result['approved'] else '⏳ Pending'}\n\n"
    
    output += "## Mission Control Team Analysis\n\n"
    for i, analysis in enumerate(result['analysis'], 1):
        output += f"### Step {i}\n{analysis}\n\n"
    
    if result['systems_status']:
        output += "## Systems Status\n\n"
        for system, status in result['systems_status'].items():
            output += f"- **{system.replace('_', ' ').title()}:** {status}\n"
    
    return output

# Create Gradio Interface
with gr.Blocks(
    title="NASA Mission Control",
    theme=gr.themes.Base(
        primary_hue="orange",
        secondary_hue="red"
    ).set(
        body_background_fill="linear-gradient(45deg, #0c0c0c, #2d1b1b)",
        panel_background_fill="rgba(255,255,255,0.05)"
    )
) as demo:
    
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #ffffff; font-size: 2.5em; margin-bottom: 10px;">
            🚀 NASA Mission Control
        </h1>
        <p style="color: #cccccc; font-size: 1.2em;">
            Advanced AI Mission Operations and Real-Time Decision Support
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            request_input = gr.Textbox(
                label="Mission Control Request",
                placeholder="e.g., 'Crew reports unusual vibration in module 2', 'Plan emergency EVA for solar panel repair', 'Orbital debris detected on collision course'",
                lines=4
            )
            
            mission_phase = gr.Dropdown(
                label="Current Mission Phase",
                choices=[
                    ("Pre-Launch", "pre_launch"),
                    ("Launch", "launch"), 
                    ("Orbital Operations", "orbital_operations"),
                    ("Docking Operations", "docking"),
                    ("EVA Operations", "eva"),
                    ("Return Prep", "return"),
                    ("Emergency", "emergency")
                ],
                value="orbital_operations"
            )
            
            process_button = gr.Button(
                "🎮 Process Mission Request",
                variant="primary",
                size="lg"
            )
            
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ffffff;">Mission Control Roles</h3>
                <ul style="color: #cccccc;">
                    <li>🎯 Mission Specialist</li>
                    <li>🔧 Systems Engineer</li>
                    <li>👨‍💼 Flight Director</li>
                </ul>
                <h4 style="color: #ffffff; margin-top: 20px;">Priority Levels</h4>
                <ul style="color: #cccccc;">
                    <li>🟢 Routine</li>
                    <li>🟡 Elevated</li>
                    <li>🟠 Critical</li>
                    <li>🔴 Emergency</li>
                </ul>
            </div>
            """)
    
    response_output = gr.Markdown(
        label="Mission Control Response",
        value="Ready for mission control operations. Enter your request above.",
        container=True
    )
    
    # Event handlers
    process_button.click(
        fn=process_mission_control_request,
        inputs=[request_input, mission_phase],
        outputs=response_output
    )
    
    request_input.submit(
        fn=process_mission_control_request,
        inputs=[request_input, mission_phase],
        outputs=response_output
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=False,  # Local-only access
        inbrowser=True
    )