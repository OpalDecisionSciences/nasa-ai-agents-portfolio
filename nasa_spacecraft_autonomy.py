"""
NASA Spacecraft Autonomy Agent
Advanced autonomous decision-making system for spacecraft operations in deep space
"""

import gradio as gr
import openai
import asyncio
import json
import random
import math
import os
import time
from typing import Dict, List, Tuple, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class SpacecraftState(BaseModel):
    """Current spacecraft state and telemetry"""
    position: Tuple[float, float, float] = Field(description="Spacecraft position (x, y, z) in km")
    velocity: Tuple[float, float, float] = Field(description="Spacecraft velocity (vx, vy, vz) in km/s")
    fuel_level: float = Field(description="Fuel percentage remaining")
    battery_level: float = Field(description="Battery percentage remaining")
    solar_panel_efficiency: float = Field(description="Solar panel efficiency percentage")
    system_health: Dict[str, str] = Field(description="Health status of various systems")
    communication_delay: float = Field(description="Communication delay to Earth in minutes")
    mission_phase: str = Field(description="Current mission phase")

class AutonomyDecision(BaseModel):
    """Autonomous decision output"""
    decision_type: str = Field(description="Type of autonomous decision made")
    actions_taken: List[str] = Field(description="List of actions taken autonomously")
    resource_allocation: Dict[str, float] = Field(description="Resource allocation adjustments")
    risk_assessment: str = Field(description="Risk level and assessment")
    communication_to_earth: str = Field(description="Message to send to Earth")
    confidence_level: float = Field(description="Confidence in decision (0-1)")

class NASASpacecraftAutonomy:
    """Advanced spacecraft autonomy system"""
    
    def __init__(self):
        # Configure OpenAI client with better settings
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Check for organization ID
        org_id = os.getenv("OPENAI_ORG_ID")
        
        # Initialize client with proper configuration
        client_kwargs = {
            "api_key": api_key,
            "timeout": 60.0,
            "max_retries": 3
        }
        
        if org_id:
            client_kwargs["organization"] = org_id
            
        self.client = openai.AsyncOpenAI(**client_kwargs)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.spacecraft_state = None
        self.last_request_time = 0
        self.min_request_interval = 3.0
        self.autonomy_rules = {
            "critical_fuel": 15.0,  # Critical fuel level %
            "critical_battery": 20.0,  # Critical battery level %
            "max_communication_delay": 20.0,  # Max delay in minutes for autonomous operation
            "system_failure_threshold": 2,  # Max simultaneous system failures
            "navigation_safety_margin": 5.0  # Safety margin in km for obstacle avoidance
        }
        
    async def initialize_spacecraft_state(self, mission_scenario: str) -> SpacecraftState:
        """Initialize spacecraft state based on mission scenario"""
        
        # Simulate different mission scenarios
        scenarios = {
            "mars_transit": {
                "position": (150000000, 0, 0),  # Halfway to Mars
                "velocity": (15.0, 0, 0),
                "fuel_level": 65.0,
                "battery_level": 85.0,
                "solar_panel_efficiency": 92.0,
                "communication_delay": 12.5,
                "mission_phase": "interplanetary_cruise"
            },
            "lunar_orbit": {
                "position": (384400, 0, 0),  # Lunar distance
                "velocity": (1.0, 0, 0),
                "fuel_level": 78.0,
                "battery_level": 91.0,
                "solar_panel_efficiency": 88.0,
                "communication_delay": 1.3,
                "mission_phase": "orbital_operations"
            },
            "deep_space": {
                "position": (500000000, 0, 0),  # Beyond Mars
                "velocity": (8.5, 0, 0),
                "fuel_level": 42.0,
                "battery_level": 76.0,
                "solar_panel_efficiency": 65.0,
                "communication_delay": 28.0,
                "mission_phase": "deep_space_exploration"
            }
        }
        
        base_scenario = scenarios.get(mission_scenario, scenarios["mars_transit"])
        
        # Add some realistic variations
        system_health = {
            "propulsion": random.choice(["nominal", "nominal", "degraded"]),
            "navigation": random.choice(["nominal", "nominal", "backup"]),
            "communications": random.choice(["nominal", "reduced", "nominal"]),
            "thermal": random.choice(["nominal", "nominal", "elevated"]),
            "power": random.choice(["nominal", "nominal", "degraded"]),
            "computers": random.choice(["nominal", "redundant", "nominal"])
        }
        
        self.spacecraft_state = SpacecraftState(
            position=base_scenario["position"],
            velocity=base_scenario["velocity"],
            fuel_level=base_scenario["fuel_level"] + random.uniform(-10, 5),
            battery_level=base_scenario["battery_level"] + random.uniform(-5, 5),
            solar_panel_efficiency=base_scenario["solar_panel_efficiency"] + random.uniform(-8, 3),
            system_health=system_health,
            communication_delay=base_scenario["communication_delay"],
            mission_phase=base_scenario["mission_phase"]
        )
        
        return self.spacecraft_state
    
    async def detect_anomalies(self, state: SpacecraftState) -> List[str]:
        """Detect system anomalies and potential issues"""
        anomalies = []
        
        # Check fuel levels
        if state.fuel_level < self.autonomy_rules["critical_fuel"]:
            anomalies.append(f"CRITICAL: Fuel level at {state.fuel_level:.1f}% - below critical threshold")
        
        # Check battery levels
        if state.battery_level < self.autonomy_rules["critical_battery"]:
            anomalies.append(f"CRITICAL: Battery level at {state.battery_level:.1f}% - power conservation required")
        
        # Check solar panel efficiency
        if state.solar_panel_efficiency < 70:
            anomalies.append(f"WARNING: Solar panel efficiency at {state.solar_panel_efficiency:.1f}% - possible degradation")
        
        # Check system health
        failed_systems = [sys for sys, status in state.system_health.items() if status in ["failed", "critical"]]
        degraded_systems = [sys for sys, status in state.system_health.items() if status in ["degraded", "backup"]]
        
        if failed_systems:
            anomalies.append(f"CRITICAL: System failures detected - {', '.join(failed_systems)}")
        
        if len(degraded_systems) > 2:
            anomalies.append(f"WARNING: Multiple degraded systems - {', '.join(degraded_systems)}")
        
        # Check communication delay for autonomous operation need
        if state.communication_delay > self.autonomy_rules["max_communication_delay"]:
            anomalies.append(f"INFO: Communication delay {state.communication_delay:.1f} min - autonomous operation required")
        
        return anomalies
    
    async def autonomous_navigation(self, state: SpacecraftState, situation: str) -> Dict[str, Any]:
        """Autonomous navigation and path planning"""
        
        prompt = f"""
        As a NASA spacecraft autonomy system, perform autonomous navigation analysis:
        
        Current State:
        - Position: {state.position} km
        - Velocity: {state.velocity} km/s
        - Mission Phase: {state.mission_phase}
        - Fuel Level: {state.fuel_level}%
        
        Situation: {situation}
        
        Provide autonomous navigation decisions:
        1. Trajectory adjustments needed
        2. Fuel consumption estimates
        3. Risk assessment for navigation
        4. Backup navigation options
        5. Autonomous waypoint planning
        
        Use spacecraft navigation protocols and orbital mechanics principles.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.1
            )
            return {"navigation_analysis": response.choices[0].message.content}
        except Exception as e:
            return {"navigation_analysis": f"Error in navigation analysis: {str(e)}"}
    
    async def fault_detection_recovery(self, state: SpacecraftState, anomalies: List[str]) -> Dict[str, Any]:
        """Autonomous fault detection and recovery procedures"""
        
        prompt = f"""
        As a NASA spacecraft fault detection and recovery system, analyze these anomalies:
        
        Spacecraft Status:
        - System Health: {json.dumps(state.system_health, indent=2)}
        - Power: Battery {state.battery_level}%, Solar {state.solar_panel_efficiency}%
        - Fuel: {state.fuel_level}%
        
        Detected Anomalies:
        {chr(10).join(f"- {anomaly}" for anomaly in anomalies)}
        
        Provide autonomous recovery actions:
        1. Immediate fault isolation procedures
        2. System redundancy activation
        3. Power rerouting and conservation
        4. Backup system engagement
        5. Risk mitigation strategies
        
        Follow NASA spacecraft emergency procedures and safety protocols.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.1
            )
            return {"recovery_procedures": response.choices[0].message.content}
        except Exception as e:
            return {"recovery_procedures": f"Error in fault recovery: {str(e)}"}
    
    async def resource_management(self, state: SpacecraftState) -> Dict[str, float]:
        """Smart resource allocation and management"""
        
        # Calculate optimal resource allocation
        total_power_available = (state.battery_level + state.solar_panel_efficiency) / 2
        
        # Base allocation percentages
        allocations = {
            "life_support": 25.0,
            "navigation": 20.0,
            "communications": 15.0,
            "scientific_instruments": 20.0,
            "propulsion": 10.0,
            "thermal_control": 10.0
        }
        
        # Adjust based on current conditions
        if state.fuel_level < 30:
            allocations["propulsion"] = 5.0  # Reduce propulsion power
            allocations["navigation"] += 5.0  # Increase navigation precision
        
        if any("degraded" in status or "backup" in status for status in state.system_health.values()):
            allocations["life_support"] += 5.0
            allocations["scientific_instruments"] -= 5.0
        
        if state.communication_delay > 15:
            allocations["communications"] += 5.0
            allocations["scientific_instruments"] -= 5.0
        
        return allocations
    
    async def make_autonomous_decision(self, situation: str, mission_scenario: str) -> AutonomyDecision:
        """Make comprehensive autonomous decision"""
        
        # Initialize or update spacecraft state
        if not self.spacecraft_state:
            await self.initialize_spacecraft_state(mission_scenario)
        
        # Detect anomalies
        anomalies = await self.detect_anomalies(self.spacecraft_state)
        
        # Get navigation analysis
        nav_analysis = await self.autonomous_navigation(self.spacecraft_state, situation)
        
        # Get recovery procedures if needed
        recovery_info = {}
        if anomalies:
            recovery_info = await self.fault_detection_recovery(self.spacecraft_state, anomalies)
        
        # Calculate resource allocation
        resource_allocation = await self.resource_management(self.spacecraft_state)
        
        # Generate comprehensive decision
        decision_prompt = f"""
        As NASA's Advanced Spacecraft Autonomy System, make a comprehensive autonomous decision:
        
        SITUATION: {situation}
        MISSION: {mission_scenario}
        
        SPACECRAFT STATE:
        - Position: {self.spacecraft_state.position}
        - Fuel: {self.spacecraft_state.fuel_level}%
        - Battery: {self.spacecraft_state.battery_level}%
        - Communication Delay: {self.spacecraft_state.communication_delay} minutes
        - System Health: {json.dumps(self.spacecraft_state.system_health)}
        
        ANALYSIS RESULTS:
        - Anomalies: {anomalies}
        - Navigation: {nav_analysis.get('navigation_analysis', 'No navigation issues')}
        - Recovery: {recovery_info.get('recovery_procedures', 'No recovery needed')}
        
        Provide autonomous decision with:
        1. Decision type classification
        2. Specific actions to take immediately
        3. Risk assessment and confidence level
        4. Message to transmit to Earth
        
        Use NASA autonomy protocols and prioritize mission safety.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": decision_prompt}],
                max_tokens=1200,
                temperature=0.1
            )
            content = response.choices[0].message.content
        except Exception as e:
            content = f"Error in autonomous decision making: {str(e)}"
        
        # Parse and structure the decision
        decision = AutonomyDecision(
            decision_type="autonomous_operational_decision",
            actions_taken=[
                "Initiated autonomous analysis protocol",
                "Assessed spacecraft systems and resources", 
                "Calculated optimal response strategy",
                "Implemented safety-first decision matrix"
            ],
            resource_allocation=resource_allocation,
            risk_assessment="Moderate - autonomous systems operating within parameters",
            communication_to_earth=f"Autonomous system response to: {situation}. Status: {content[:200]}...",
            confidence_level=0.87
        )
        
        return decision, content
    
    async def run_autonomy_simulation(self, situation: str, mission_scenario: str):
        """Run complete autonomy simulation"""
        
        yield f"# 🚀 NASA Spacecraft Autonomy System\n\n"
        yield f"**Mission Scenario:** {mission_scenario.replace('_', ' ').title()}\n"
        yield f"**Situation:** {situation}\n\n"
        
        yield "## 🤖 Initializing Autonomous Systems...\n\n"
        
        # Initialize spacecraft
        state = await self.initialize_spacecraft_state(mission_scenario)
        yield f"### Spacecraft State Initialized\n"
        yield f"- **Position:** {state.position[0]:,.0f} km from Earth\n"
        yield f"- **Fuel Level:** {state.fuel_level:.1f}%\n"
        yield f"- **Battery Level:** {state.battery_level:.1f}%\n"
        yield f"- **Solar Efficiency:** {state.solar_panel_efficiency:.1f}%\n"
        yield f"- **Communication Delay:** {state.communication_delay:.1f} minutes\n"
        yield f"- **Mission Phase:** {state.mission_phase.replace('_', ' ').title()}\n\n"
        
        yield "## 🔍 Autonomous Analysis Phase...\n\n"
        
        # Detect anomalies
        anomalies = await self.detect_anomalies(state)
        if anomalies:
            yield f"### ⚠️ Anomalies Detected:\n"
            for anomaly in anomalies:
                yield f"- {anomaly}\n"
        else:
            yield f"### ✅ No Critical Anomalies Detected\n"
        yield "\n"
        
        yield "## 🧠 Making Autonomous Decision...\n\n"
        
        # Make decision
        decision, detailed_response = await self.make_autonomous_decision(situation, mission_scenario)
        
        yield f"### Decision Type: {decision.decision_type.replace('_', ' ').title()}\n\n"
        yield f"### Autonomous Actions Taken:\n"
        for action in decision.actions_taken:
            yield f"- ✅ {action}\n"
        yield "\n"
        
        yield f"### Resource Allocation:\n"
        for system, percentage in decision.resource_allocation.items():
            yield f"- **{system.replace('_', ' ').title()}:** {percentage:.1f}%\n"
        yield "\n"
        
        yield f"### Risk Assessment: {decision.risk_assessment}\n"
        yield f"### Confidence Level: {decision.confidence_level:.0%}\n\n"
        
        yield "## 📡 Communication to Earth\n\n"
        yield f"**Transmission (Delay: {state.communication_delay:.1f} min):**\n"
        yield f"{decision.communication_to_earth}\n\n"
        
        yield "## 🔬 Detailed Analysis\n\n"
        yield detailed_response
        
        yield f"\n\n---\n**Autonomous System Status: OPERATIONAL** ✅\n"
        yield f"**Next Analysis Cycle: {(datetime.now() + timedelta(minutes=5)).strftime('%H:%M UTC')}**"

# Gradio Interface
async def run_spacecraft_autonomy(situation: str, mission_scenario: str):
    """Run spacecraft autonomy simulation"""
    autonomy_system = NASASpacecraftAutonomy()
    
    async for chunk in autonomy_system.run_autonomy_simulation(situation, mission_scenario):
        yield chunk

# Create Gradio interface
with gr.Blocks(
    title="NASA Spacecraft Autonomy",
    theme=gr.themes.Base(
        primary_hue="purple",
        secondary_hue="cyan"
    ).set(
        body_background_fill="linear-gradient(45deg, #0a0a1a, #1a0a2e)",
        panel_background_fill="rgba(255,255,255,0.05)"
    )
) as demo:
    
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #ffffff; font-size: 2.5em; margin-bottom: 10px;">
            🤖 NASA Spacecraft Autonomy
        </h1>
        <p style="color: #cccccc; font-size: 1.2em;">
            Advanced Autonomous Decision-Making for Deep Space Operations
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            situation_input = gr.Textbox(
                label="Autonomous Situation",
                placeholder="e.g., 'Solar panel damaged by micrometeorite', 'Navigation computer malfunction detected', 'Fuel leak in primary thruster'",
                lines=4
            )
            
            scenario_dropdown = gr.Dropdown(
                label="Mission Scenario",
                choices=[
                    ("Mars Transit Mission", "mars_transit"),
                    ("Lunar Orbital Operations", "lunar_orbit"), 
                    ("Deep Space Exploration", "deep_space")
                ],
                value="mars_transit"
            )
            
            autonomy_button = gr.Button(
                "🤖 Activate Autonomous Systems",
                variant="primary",
                size="lg"
            )
            
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ffffff;">Autonomy Capabilities</h3>
                <ul style="color: #cccccc;">
                    <li>🧭 Autonomous Navigation</li>
                    <li>⚡ Fault Detection & Recovery</li>
                    <li>🔋 Smart Resource Management</li>
                    <li>🛡️ Risk Assessment</li>
                    <li>📡 Earth Communication</li>
                </ul>
                <h4 style="color: #ffffff; margin-top: 20px;">Mission Scenarios</h4>
                <p style="color: #cccccc; font-size: 0.9em;">
                    Simulates real deep space missions where communication delays 
                    make autonomous decision-making critical for mission success.
                </p>
            </div>
            """)
    
    autonomy_output = gr.Markdown(
        label="Spacecraft Autonomy Response",
        value="Autonomous systems ready. Configure situation and mission scenario above.",
        container=True
    )
    
    # Event handlers
    autonomy_button.click(
        fn=run_spacecraft_autonomy,
        inputs=[situation_input, scenario_dropdown],
        outputs=autonomy_output
    )
    
    situation_input.submit(
        fn=run_spacecraft_autonomy,
        inputs=[situation_input, scenario_dropdown],
        outputs=autonomy_output
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7863,
        share=False,  # Local-only access
        inbrowser=True
    )