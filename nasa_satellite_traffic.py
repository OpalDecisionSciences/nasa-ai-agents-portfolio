"""
NASA Satellite and Orbital Traffic Management Agent
Advanced AI system for orbital collision avoidance and space traffic coordination
"""

import gradio as gr
import openai
import asyncio
import json
import random
import math
import os
import time
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class SatelliteObject(BaseModel):
    """Satellite or space object representation"""
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Object name")
    object_type: str = Field(description="Type: satellite, debris, spacecraft")
    position: Tuple[float, float, float] = Field(description="Position in km (x, y, z)")
    velocity: Tuple[float, float, float] = Field(description="Velocity in km/s (vx, vy, vz)")
    altitude: float = Field(description="Orbital altitude in km")
    inclination: float = Field(description="Orbital inclination in degrees")
    mass: float = Field(description="Object mass in kg")
    cross_section: float = Field(description="Cross-sectional area in m²")
    owner: str = Field(description="Operator or country")
    mission_status: str = Field(description="Active, inactive, or debris")

class CollisionRisk(BaseModel):
    """Collision risk assessment"""
    primary_object: str = Field(description="Primary object ID")
    secondary_object: str = Field(description="Secondary object ID") 
    time_to_closest_approach: float = Field(description="Time to closest approach in hours")
    minimum_distance: float = Field(description="Minimum distance in km")
    collision_probability: float = Field(description="Collision probability (0-1)")
    risk_level: str = Field(description="Risk level: low, medium, high, critical")
    recommended_action: str = Field(description="Recommended action")

class ManeuverPlan(BaseModel):
    """Orbital maneuver plan"""
    object_id: str = Field(description="Object to maneuver")
    maneuver_type: str = Field(description="Type of maneuver")
    delta_v_required: float = Field(description="Delta-V required in m/s")
    maneuver_time: str = Field(description="When to execute maneuver")
    fuel_cost: float = Field(description="Fuel cost in kg")
    success_probability: float = Field(description="Success probability")
    alternatives: List[str] = Field(description="Alternative options")

class NASASatelliteTrafficManager:
    """Advanced orbital traffic management system"""
    
    def __init__(self):
        # Configure OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        client_kwargs = {"api_key": api_key, "timeout": 60.0, "max_retries": 3}
        org_id = os.getenv("OPENAI_ORG_ID")
        if org_id:
            client_kwargs["organization"] = org_id
            
        self.client = openai.AsyncOpenAI(**client_kwargs)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.tracked_objects = []
        self.collision_risks = []
        self.orbital_zones = {
            "LEO": {"min_alt": 160, "max_alt": 2000, "congestion": "high"},
            "MEO": {"min_alt": 2000, "max_alt": 35786, "congestion": "medium"},
            "GEO": {"min_alt": 35786, "max_alt": 35886, "congestion": "high"},
            "HEO": {"min_alt": 35886, "max_alt": 100000, "congestion": "low"}
        }
        
    def generate_orbital_population(self, zone: str = "LEO") -> List[SatelliteObject]:
        """Generate realistic orbital population for simulation"""
        objects = []
        
        zone_params = self.orbital_zones.get(zone, self.orbital_zones["LEO"])
        base_altitude = (zone_params["min_alt"] + zone_params["max_alt"]) / 2
        
        # Active satellites
        satellite_types = [
            ("Starlink", "communications", "SpaceX", 260),
            ("OneWeb", "communications", "OneWeb", 185), 
            ("ISS", "space_station", "International", 408),
            ("Hubble", "observatory", "NASA", 547),
            ("GPS", "navigation", "US_Military", 20200),
            ("Weather_Sat", "meteorology", "NOAA", 850),
            ("Earth_Obs", "observation", "ESA", 705)
        ]
        
        for i, (name, obj_type, owner, alt) in enumerate(satellite_types):
            if zone_params["min_alt"] <= alt <= zone_params["max_alt"]:
                # Generate orbital parameters
                inclination = random.uniform(0, 180)
                velocity_magnitude = math.sqrt(398600 / (6371 + alt))  # Orbital velocity
                
                objects.append(SatelliteObject(
                    id=f"SAT-{i+1:03d}",
                    name=name,
                    object_type="satellite",
                    position=(
                        (6371 + alt) * math.cos(random.uniform(0, 2*math.pi)),
                        (6371 + alt) * math.sin(random.uniform(0, 2*math.pi)),
                        random.uniform(-1000, 1000)
                    ),
                    velocity=(
                        velocity_magnitude * random.uniform(-0.1, 0.1),
                        velocity_magnitude * (1 + random.uniform(-0.05, 0.05)),
                        random.uniform(-0.5, 0.5)
                    ),
                    altitude=alt,
                    inclination=inclination,
                    mass=random.uniform(100, 15000),
                    cross_section=random.uniform(5, 100),
                    owner=owner,
                    mission_status="active"
                ))
        
        # Add space debris
        debris_count = random.randint(15, 25)
        for i in range(debris_count):
            alt = random.uniform(zone_params["min_alt"], zone_params["max_alt"])
            velocity_magnitude = math.sqrt(398600 / (6371 + alt))
            
            objects.append(SatelliteObject(
                id=f"DEB-{i+1:03d}",
                name=f"Debris_{i+1}",
                object_type="debris",
                position=(
                    (6371 + alt) * math.cos(random.uniform(0, 2*math.pi)),
                    (6371 + alt) * math.sin(random.uniform(0, 2*math.pi)),
                    random.uniform(-2000, 2000)
                ),
                velocity=(
                    velocity_magnitude * random.uniform(-0.2, 0.2),
                    velocity_magnitude * (1 + random.uniform(-0.1, 0.1)),
                    random.uniform(-1, 1)
                ),
                altitude=alt,
                inclination=random.uniform(0, 180),
                mass=random.uniform(0.1, 500),
                cross_section=random.uniform(0.01, 10),
                owner="Unknown",
                mission_status="debris"
            ))
        
        return objects
    
    async def predict_trajectories(self, objects: List[SatelliteObject], hours_ahead: float = 24) -> Dict[str, List[Tuple[float, float, float]]]:
        """Predict orbital trajectories for collision analysis"""
        
        trajectories = {}
        
        for obj in objects:
            trajectory = []
            current_pos = obj.position
            current_vel = obj.velocity
            
            # Simple orbital propagation (simplified for demo)
            time_steps = int(hours_ahead * 10)  # 6-minute intervals
            dt = hours_ahead * 3600 / time_steps  # seconds per step
            
            for step in range(time_steps):
                # Simplified two-body orbital mechanics
                r = math.sqrt(sum(x**2 for x in current_pos))
                
                # Gravitational acceleration
                mu = 398600  # Earth's gravitational parameter
                a_grav = [-mu * x / (r**3) for x in current_pos]
                
                # Update velocity and position
                current_vel = tuple(v + a * dt for v, a in zip(current_vel, a_grav))
                current_pos = tuple(p + v * dt for p, v in zip(current_pos, current_vel))
                
                trajectory.append(current_pos)
            
            trajectories[obj.id] = trajectory
        
        return trajectories
    
    async def assess_collision_risks(self, objects: List[SatelliteObject]) -> List[CollisionRisk]:
        """Assess collision risks between all objects"""
        
        risks = []
        trajectories = await self.predict_trajectories(objects)
        
        # Check all pairs of objects
        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects[i+1:], i+1):
                
                traj1 = trajectories[obj1.id]
                traj2 = trajectories[obj2.id]
                
                min_distance = float('inf')
                min_time = 0
                
                # Find closest approach
                for t, (pos1, pos2) in enumerate(zip(traj1, traj2)):
                    distance = math.sqrt(sum((p1-p2)**2 for p1, p2 in zip(pos1, pos2)))
                    if distance < min_distance:
                        min_distance = distance
                        min_time = t * 0.1  # Convert to hours
                
                # Calculate collision probability (simplified)
                combined_cross_section = math.sqrt(obj1.cross_section + obj2.cross_section)
                collision_prob = max(0, 1 - (min_distance / (combined_cross_section / 1000)))
                
                # Determine risk level
                if collision_prob > 0.1 or min_distance < 1:
                    risk_level = "critical"
                elif collision_prob > 0.01 or min_distance < 5:
                    risk_level = "high"
                elif collision_prob > 0.001 or min_distance < 25:
                    risk_level = "medium"
                else:
                    risk_level = "low"
                
                if risk_level in ["medium", "high", "critical"]:
                    risks.append(CollisionRisk(
                        primary_object=obj1.id,
                        secondary_object=obj2.id,
                        time_to_closest_approach=min_time,
                        minimum_distance=min_distance,
                        collision_probability=collision_prob,
                        risk_level=risk_level,
                        recommended_action=f"Monitor closely" if risk_level == "medium" else "Consider avoidance maneuver"
                    ))
        
        return sorted(risks, key=lambda x: x.collision_probability, reverse=True)
    
    async def plan_avoidance_maneuver(self, risk: CollisionRisk, objects: List[SatelliteObject]) -> ManeuverPlan:
        """Plan collision avoidance maneuver"""
        
        # Find the objects involved
        obj1 = next(obj for obj in objects if obj.id == risk.primary_object)
        obj2 = next(obj for obj in objects if obj.id == risk.secondary_object)
        
        # Choose which object to maneuver (prefer active satellites over debris)
        if obj1.mission_status == "active" and obj2.mission_status != "active":
            maneuver_obj = obj1
        elif obj2.mission_status == "active" and obj1.mission_status != "active":
            maneuver_obj = obj2
        else:
            # Both or neither active, choose based on mass/capability
            maneuver_obj = obj1 if obj1.mass > obj2.mass else obj2
        
        # Calculate required delta-V (simplified)
        base_delta_v = 50 + (100 * risk.collision_probability)  # m/s
        fuel_cost = base_delta_v * maneuver_obj.mass * 0.01  # Rough estimate
        
        # Determine maneuver timing
        maneuver_time = datetime.now() + timedelta(hours=max(1, risk.time_to_closest_approach - 2))
        
        prompt = f"""
        As NASA's orbital mechanics specialist, plan a collision avoidance maneuver:
        
        COLLISION RISK:
        - Objects: {obj1.name} ({obj1.id}) and {obj2.name} ({obj2.id})
        - Minimum Distance: {risk.minimum_distance:.2f} km
        - Collision Probability: {risk.collision_probability:.4f}
        - Time to Approach: {risk.time_to_closest_approach:.1f} hours
        
        SELECTED OBJECT FOR MANEUVER: {maneuver_obj.name}
        - Mass: {maneuver_obj.mass:.0f} kg
        - Altitude: {maneuver_obj.altitude:.0f} km
        - Current Status: {maneuver_obj.mission_status}
        
        Provide detailed maneuver recommendation including:
        1. Optimal maneuver type (radial, tangential, normal)
        2. Precise timing and execution
        3. Alternative maneuver options
        4. Risk assessment and success probability
        
        Use orbital mechanics principles and NASA collision avoidance protocols.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.1
            )
        except Exception as e:
            # Return error fallback
            response = type('obj', (object,), {
                'choices': [type('obj', (object,), {
                    'message': type('obj', (object,), {
                        'content': f"Error in maneuver planning: {str(e)}"
                    })()
                })()]
            })()
        
        return ManeuverPlan(
            object_id=maneuver_obj.id,
            maneuver_type="collision_avoidance",
            delta_v_required=base_delta_v,
            maneuver_time=maneuver_time.strftime("%Y-%m-%d %H:%M UTC"),
            fuel_cost=fuel_cost,
            success_probability=0.95,
            alternatives=[
                "Delay maneuver by 30 minutes",
                "Alternative trajectory adjustment",
                "Coordinate with other object operator"
            ]
        ), response.choices[0].message.content
    
    async def coordinate_constellation_management(self, scenario: str) -> str:
        """Coordinate multiple satellites in constellations"""
        
        prompt = f"""
        As NASA's satellite constellation coordination specialist, manage this scenario:
        
        SCENARIO: {scenario}
        
        Provide constellation management strategy including:
        1. Multi-satellite coordination protocols
        2. Automated collision avoidance between constellation members
        3. Formation flying and spacing optimization
        4. Ground control communication priorities
        5. Autonomous decision-making protocols
        
        Consider Starlink, OneWeb, and other mega-constellations operating in similar orbits.
        Use NASA's space traffic management best practices.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in constellation management: {str(e)}"
    
    async def run_traffic_management(self, scenario: str, orbital_zone: str):
        """Run complete orbital traffic management simulation"""
        
        yield f"# 🛰️ NASA Satellite Traffic Management System\n\n"
        yield f"**Scenario:** {scenario}\n"
        yield f"**Orbital Zone:** {orbital_zone} ({self.orbital_zones[orbital_zone]['min_alt']}-{self.orbital_zones[orbital_zone]['max_alt']} km)\n"
        yield f"**Congestion Level:** {self.orbital_zones[orbital_zone]['congestion'].upper()}\n\n"
        
        yield "## 📡 Initializing Orbital Surveillance...\n\n"
        
        # Generate orbital population
        objects = self.generate_orbital_population(orbital_zone)
        active_sats = [obj for obj in objects if obj.mission_status == "active"]
        debris_objects = [obj for obj in objects if obj.mission_status == "debris"]
        
        yield f"### Current Orbital Population\n"
        yield f"- **Active Satellites:** {len(active_sats)}\n"
        yield f"- **Space Debris:** {len(debris_objects)}\n"
        yield f"- **Total Tracked Objects:** {len(objects)}\n\n"
        
        yield "### Major Satellites Tracked:\n"
        for obj in active_sats[:5]:
            yield f"- **{obj.name}** ({obj.id}) - {obj.altitude:.0f} km - {obj.owner}\n"
        yield "\n"
        
        yield "## ⚠️ Collision Risk Assessment...\n\n"
        
        risks = await self.assess_collision_risks(objects)
        high_risks = [r for r in risks if r.risk_level in ["high", "critical"]]
        
        if high_risks:
            yield f"### 🚨 High-Priority Collision Risks: {len(high_risks)}\n\n"
            for risk in high_risks[:3]:
                obj1 = next(obj for obj in objects if obj.id == risk.primary_object)
                obj2 = next(obj for obj in objects if obj.id == risk.secondary_object)
                yield f"**Risk #{risks.index(risk)+1}** - {risk.risk_level.upper()}\n"
                yield f"- Objects: {obj1.name} ↔ {obj2.name}\n"
                yield f"- Closest Approach: {risk.minimum_distance:.2f} km in {risk.time_to_closest_approach:.1f} hours\n"
                yield f"- Collision Probability: {risk.collision_probability:.4f}\n"
                yield f"- Action: {risk.recommended_action}\n\n"
        else:
            yield f"### ✅ No High-Priority Collision Risks Detected\n\n"
            yield f"**Medium/Low Risks:** {len(risks)} monitored situations\n\n"
        
        yield "## 🚀 Collision Avoidance Planning...\n\n"
        
        if high_risks:
            # Plan maneuver for highest risk
            top_risk = high_risks[0]
            maneuver_plan, detailed_analysis = await self.plan_avoidance_maneuver(top_risk, objects)
            
            yield f"### Avoidance Maneuver Plan\n"
            yield f"- **Target Object:** {maneuver_plan.object_id}\n"
            yield f"- **Maneuver Type:** {maneuver_plan.maneuver_type.replace('_', ' ').title()}\n"
            yield f"- **Delta-V Required:** {maneuver_plan.delta_v_required:.1f} m/s\n"
            yield f"- **Execution Time:** {maneuver_plan.maneuver_time}\n"
            yield f"- **Fuel Cost:** {maneuver_plan.fuel_cost:.1f} kg\n"
            yield f"- **Success Probability:** {maneuver_plan.success_probability:.0%}\n\n"
            
            yield "### Detailed Analysis\n"
            yield detailed_analysis + "\n\n"
        
        yield "## 🌐 Constellation Coordination...\n\n"
        
        constellation_analysis = await self.coordinate_constellation_management(scenario)
        yield constellation_analysis + "\n\n"
        
        yield "## 📊 Traffic Management Summary\n\n"
        yield f"- **Objects Tracked:** {len(objects)}\n"
        yield f"- **Collision Risks Identified:** {len(risks)}\n"
        yield f"- **Critical Risks:** {len([r for r in risks if r.risk_level == 'critical'])}\n"
        yield f"- **Maneuvers Planned:** {1 if high_risks else 0}\n"
        yield f"- **System Status:** {'⚠️ ACTIVE MONITORING' if high_risks else '✅ NOMINAL'}\n\n"
        
        yield f"---\n**Next Update:** {(datetime.now() + timedelta(minutes=15)).strftime('%H:%M UTC')}**"

# Gradio Interface
async def run_satellite_traffic_management(scenario: str, orbital_zone: str):
    """Run satellite traffic management simulation"""
    traffic_manager = NASASatelliteTrafficManager()
    
    async for chunk in traffic_manager.run_traffic_management(scenario, orbital_zone):
        yield chunk

# Create Gradio interface
with gr.Blocks(
    title="NASA Satellite Traffic Management",
    theme=gr.themes.Base(
        primary_hue="green",
        secondary_hue="blue"
    ).set(
        body_background_fill="linear-gradient(45deg, #0a1a0a, #1a2a1a)",
        panel_background_fill="rgba(255,255,255,0.05)"
    )
) as demo:
    
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #ffffff; font-size: 2.5em; margin-bottom: 10px;">
            🛰️ NASA Satellite Traffic Management
        </h1>
        <p style="color: #cccccc; font-size: 1.2em;">
            Advanced Orbital Collision Avoidance and Space Traffic Coordination
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            scenario_input = gr.Textbox(
                label="Traffic Management Scenario",
                placeholder="e.g., 'Large debris field detected in Starlink constellation orbit', 'Multiple satellite constellation coordination needed', 'Emergency maneuver required for ISS debris avoidance'",
                lines=4
            )
            
            zone_dropdown = gr.Dropdown(
                label="Orbital Zone",
                choices=[
                    ("Low Earth Orbit (LEO) - 160-2000 km", "LEO"),
                    ("Medium Earth Orbit (MEO) - 2000-35786 km", "MEO"),
                    ("Geostationary Orbit (GEO) - 35786 km", "GEO"),
                    ("High Earth Orbit (HEO) - >35886 km", "HEO")
                ],
                value="LEO"
            )
            
            traffic_button = gr.Button(
                "🛰️ Activate Traffic Management",
                variant="primary",
                size="lg"
            )
            
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ffffff;">Traffic Management</h3>
                <ul style="color: #cccccc;">
                    <li>🎯 Trajectory Prediction</li>
                    <li>⚠️ Collision Risk Assessment</li>
                    <li>🚀 Avoidance Maneuvers</li>
                    <li>🌐 Constellation Coordination</li>
                    <li>📡 Multi-Satellite Management</li>
                </ul>
                <h4 style="color: #ffffff; margin-top: 20px;">Orbital Zones</h4>
                <ul style="color: #cccccc; font-size: 0.9em;">
                    <li>LEO: Most congested</li>
                    <li>MEO: GPS, navigation</li>
                    <li>GEO: Communications</li>
                    <li>HEO: Deep space missions</li>
                </ul>
            </div>
            """)
    
    traffic_output = gr.Markdown(
        label="Traffic Management Response",
        value="Space traffic management system ready. Configure scenario and orbital zone above.",
        container=True
    )
    
    # Event handlers
    traffic_button.click(
        fn=run_satellite_traffic_management,
        inputs=[scenario_input, zone_dropdown],
        outputs=traffic_output
    )
    
    scenario_input.submit(
        fn=run_satellite_traffic_management,
        inputs=[scenario_input, zone_dropdown],
        outputs=traffic_output
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7864,
        share=False,  # Local-only access
        inbrowser=True
    )