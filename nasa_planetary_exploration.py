"""
NASA Planetary Exploration and Mapping Agent
Advanced AI system for autonomous planetary surface analysis and exploration planning
"""

import gradio as gr
import openai
import asyncio
import json
import random
import base64
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

class TerrainFeature(BaseModel):
    """Geological or surface feature"""
    feature_id: str = Field(description="Unique identifier")
    feature_type: str = Field(description="Type: crater, rock, mineral, water_ice, etc.")
    location: Tuple[float, float] = Field(description="Coordinates (lat, lon)")
    size: float = Field(description="Size in meters")
    composition: str = Field(description="Material composition")
    scientific_interest: float = Field(description="Scientific interest score 0-10")
    accessibility: str = Field(description="Rover accessibility: easy, moderate, difficult")
    hazard_level: str = Field(description="Hazard level: low, medium, high")

class ExplorationTarget(BaseModel):
    """Scientific exploration target"""
    target_id: str = Field(description="Target identifier")
    priority: str = Field(description="Priority: high, medium, low")
    target_type: str = Field(description="Type of investigation")
    coordinates: Tuple[float, float] = Field(description="Target coordinates")
    estimated_duration: float = Field(description="Investigation time in sols")
    required_instruments: List[str] = Field(description="Required instruments")
    scientific_objectives: List[str] = Field(description="Scientific objectives")
    risk_factors: List[str] = Field(description="Associated risks")

class PathPlan(BaseModel):
    """Rover path planning"""
    path_id: str = Field(description="Path identifier")
    waypoints: List[Tuple[float, float]] = Field(description="Path waypoints")
    total_distance: float = Field(description="Total distance in meters")
    estimated_time: float = Field(description="Estimated travel time in sols")
    energy_required: float = Field(description="Energy required in Wh")
    hazards_avoided: List[str] = Field(description="Hazards avoided")
    alternative_paths: int = Field(description="Number of alternative paths")

class NASAPlanetaryExplorer:
    """Advanced planetary exploration and mapping system"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI()
        self.planetary_bodies = {
            "mars": {
                "gravity": 3.71,
                "day_length": 24.6,
                "atmosphere": "thin_co2",
                "temperature_range": (-195, 20),
                "key_features": ["polar_ice", "canyons", "volcanoes", "impact_craters"],
                "missions": ["Perseverance", "Curiosity", "Ingenuity"]
            },
            "moon": {
                "gravity": 1.62,
                "day_length": 708,
                "atmosphere": "none",
                "temperature_range": (-230, 120),
                "key_features": ["craters", "maria", "highlands", "ice_deposits"],
                "missions": ["Apollo", "Artemis", "Chang'e"]
            },
            "europa": {
                "gravity": 1.31,
                "day_length": 85.2,
                "atmosphere": "thin_oxygen",
                "temperature_range": (-223, -148),
                "key_features": ["ice_shell", "subsurface_ocean", "chaos_terrain"],
                "missions": ["Europa_Clipper", "JUICE"]
            }
        }
        
    async def analyze_terrain_image(self, planetary_body: str, region_description: str) -> List[TerrainFeature]:
        """Simulate advanced terrain analysis from orbital/surface imagery"""
        
        body_info = self.planetary_bodies.get(planetary_body, self.planetary_bodies["mars"])
        
        prompt = f"""
        As NASA's planetary geology AI specialist, analyze terrain imagery for {planetary_body}:
        
        REGION: {region_description}
        PLANETARY CONTEXT:
        - Gravity: {body_info['gravity']} m/s²
        - Key Features: {', '.join(body_info['key_features'])}
        - Active Missions: {', '.join(body_info['missions'])}
        
        Identify and catalog terrain features including:
        1. Geological formations and their significance
        2. Potential mineral compositions
        3. Evidence of past/present water activity
        4. Impact craters and their ages
        5. Volcanic or tectonic features
        6. Hazards for rover operations
        7. Scientifically interesting targets
        
        For each feature, assess:
        - Scientific importance (1-10 scale)
        - Accessibility for rover investigation
        - Potential risks and hazards
        - Required instruments for analysis
        
        Use established planetary geology terminology and NASA exploration protocols.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200
        )
        
        # Generate realistic terrain features based on analysis
        features = []
        feature_types = {
            "mars": ["crater", "rock_formation", "mineral_vein", "ancient_riverbed", "dust_devil_track"],
            "moon": ["impact_crater", "boulder", "regolith_sample", "ice_deposit", "lava_tube"],
            "europa": ["ice_ridge", "chaos_terrain", "thermal_anomaly", "subsurface_feature", "impact_crater"]
        }
        
        types_list = feature_types.get(planetary_body, feature_types["mars"])
        
        for i in range(random.randint(5, 8)):
            features.append(TerrainFeature(
                feature_id=f"{planetary_body.upper()}-F{i+1:03d}",
                feature_type=random.choice(types_list),
                location=(
                    random.uniform(-45, 45),  # latitude
                    random.uniform(-180, 180)  # longitude
                ),
                size=random.uniform(0.5, 50.0),
                composition=random.choice([
                    "basaltic_rock", "sedimentary_layers", "iron_oxide", 
                    "water_ice", "sulfate_minerals", "carbonates"
                ]),
                scientific_interest=random.uniform(3.0, 9.5),
                accessibility=random.choice(["easy", "easy", "moderate", "difficult"]),
                hazard_level=random.choice(["low", "low", "medium", "high"])
            ))
        
        return features, response.choices[0].message.content
    
    async def prioritize_targets(self, features: List[TerrainFeature], mission_objectives: List[str]) -> List[ExplorationTarget]:
        """Prioritize exploration targets based on scientific value and mission objectives"""
        
        prompt = f"""
        As NASA's mission planning specialist, prioritize these terrain features for exploration:
        
        MISSION OBJECTIVES:
        {chr(10).join(f"- {obj}" for obj in mission_objectives)}
        
        TERRAIN FEATURES:
        {chr(10).join(f"- {f.feature_type} at {f.location} - Interest: {f.scientific_interest}/10, Access: {f.accessibility}" for f in features)}
        
        Create prioritized exploration targets considering:
        1. Scientific value and mission relevance
        2. Accessibility and operational feasibility
        3. Risk vs. reward analysis
        4. Instrument requirements and capabilities
        5. Time and energy constraints
        6. Backup target options
        
        For each target, specify:
        - Priority level and justification
        - Required investigation duration
        - Necessary instruments and procedures
        - Associated risks and mitigation strategies
        
        Use NASA planetary exploration best practices.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        # Generate exploration targets based on features
        targets = []
        high_interest_features = [f for f in features if f.scientific_interest > 7.0]
        accessible_features = [f for f in features if f.accessibility in ["easy", "moderate"]]
        
        # Combine high interest and accessible features
        priority_features = list(set(high_interest_features + accessible_features))[:6]
        
        for i, feature in enumerate(priority_features):
            priority = "high" if feature.scientific_interest > 8.0 and feature.accessibility == "easy" else \
                     "medium" if feature.scientific_interest > 6.0 else "low"
            
            targets.append(ExplorationTarget(
                target_id=f"TGT-{i+1:02d}",
                priority=priority,
                target_type=f"{feature.feature_type}_investigation",
                coordinates=feature.location,
                estimated_duration=random.uniform(0.5, 3.0),
                required_instruments=[
                    "cameras", "spectrometer", 
                    random.choice(["drill", "arm", "laser", "microscope"])
                ],
                scientific_objectives=[
                    f"Analyze {feature.composition}",
                    f"Determine {feature.feature_type} formation process",
                    "Collect geological context"
                ],
                risk_factors=["terrain_difficulty"] if feature.accessibility == "difficult" else []
            ))
        
        return targets, response.choices[0].message.content
    
    async def plan_rover_path(self, targets: List[ExplorationTarget], rover_position: Tuple[float, float]) -> PathPlan:
        """Plan optimal rover path between exploration targets"""
        
        prompt = f"""
        As NASA's rover operations specialist, plan an optimal path for surface exploration:
        
        CURRENT ROVER POSITION: {rover_position}
        
        EXPLORATION TARGETS:
        {chr(10).join(f"- {t.target_id}: {t.target_type} at {t.coordinates} (Priority: {t.priority})" for t in targets)}
        
        Plan the most efficient path considering:
        1. Travel distance and energy consumption
        2. Target priority and scientific value
        3. Terrain hazards and accessibility
        4. Backup routes and contingency options
        5. Communication windows and power constraints
        6. Weather patterns and seasonal considerations
        
        Provide:
        - Optimal waypoint sequence
        - Distance and time estimates
        - Energy requirements and charging stops
        - Hazard avoidance strategies
        - Alternative path options
        
        Use NASA rover operations protocols and planetary navigation techniques.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        
        # Generate realistic path planning
        high_priority_targets = [t for t in targets if t.priority == "high"][:4]
        
        # Create waypoints (simplified path planning)
        waypoints = [rover_position]
        for target in high_priority_targets:
            waypoints.append(target.coordinates)
        
        # Calculate approximate distances
        total_distance = 0
        for i in range(len(waypoints)-1):
            # Simplified distance calculation
            lat_diff = waypoints[i+1][0] - waypoints[i][0]
            lon_diff = waypoints[i+1][1] - waypoints[i][1]
            distance = ((lat_diff**2 + lon_diff**2)**0.5) * 111000  # rough meters
            total_distance += distance
        
        path_plan = PathPlan(
            path_id=f"PATH-{datetime.now().strftime('%Y%m%d')}",
            waypoints=waypoints,
            total_distance=total_distance,
            estimated_time=total_distance / 100,  # Rough estimate: 100m per sol
            energy_required=total_distance * 0.1,  # Rough estimate: 0.1 Wh per meter
            hazards_avoided=["steep_slopes", "loose_rocks", "sand_traps"],
            alternative_paths=2
        )
        
        return path_plan, response.choices[0].message.content
    
    async def autonomous_science_selection(self, available_time: float, targets: List[ExplorationTarget]) -> Dict[str, Any]:
        """Autonomous selection of science activities based on available time and conditions"""
        
        prompt = f"""
        As NASA's autonomous science planning AI, select optimal science activities:
        
        AVAILABLE TIME: {available_time} sols
        
        POTENTIAL TARGETS:
        {chr(10).join(f"- {t.target_id}: {t.target_type} ({t.priority} priority, {t.estimated_duration} sols)" for t in targets)}
        
        Autonomously select and schedule science activities considering:
        1. Time constraints and energy budgets
        2. Scientific priority and mission objectives
        3. Instrument availability and health
        4. Environmental conditions (dust, temperature, lighting)
        5. Data storage and transmission opportunities
        6. Backup activities for contingencies
        
        Provide:
        - Selected targets and scheduling
        - Instrument usage optimization
        - Data collection priorities
        - Contingency science plans
        - Risk assessment and mitigation
        
        Use NASA's autonomous science protocols and adaptive mission planning.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        # Select targets that fit within time constraints
        selected_targets = []
        remaining_time = available_time
        
        # Sort by priority and duration
        sorted_targets = sorted(targets, key=lambda x: (x.priority == "high", -x.estimated_duration))
        
        for target in sorted_targets:
            if target.estimated_duration <= remaining_time:
                selected_targets.append(target)
                remaining_time -= target.estimated_duration
                if remaining_time <= 0:
                    break
        
        return {
            "selected_targets": selected_targets,
            "total_duration": available_time - remaining_time,
            "utilization": ((available_time - remaining_time) / available_time) * 100,
            "analysis": response.choices[0].message.content
        }
    
    async def run_exploration_mission(self, planetary_body: str, region: str, mission_objectives: List[str]):
        """Run complete planetary exploration mission simulation"""
        
        yield f"# 🌍 NASA Planetary Exploration Mission\n\n"
        yield f"**Target:** {planetary_body.title()}\n"
        yield f"**Region:** {region}\n"
        yield f"**Mission Duration:** 90 sols (planned)\n\n"
        
        body_info = self.planetary_bodies.get(planetary_body, self.planetary_bodies["mars"])
        yield f"### Planetary Environment\n"
        yield f"- **Gravity:** {body_info['gravity']} m/s²\n"
        yield f"- **Day Length:** {body_info['day_length']} hours\n"
        yield f"- **Atmosphere:** {body_info['atmosphere'].replace('_', ' ').title()}\n"
        yield f"- **Temperature:** {body_info['temperature_range'][0]}°C to {body_info['temperature_range'][1]}°C\n\n"
        
        yield f"### Mission Objectives\n"
        for obj in mission_objectives:
            yield f"- {obj}\n"
        yield "\n"
        
        yield "## 🔍 Terrain Analysis Phase...\n\n"
        
        # Analyze terrain
        features, terrain_analysis = await self.analyze_terrain_image(planetary_body, region)
        yield f"### Terrain Features Identified: {len(features)}\n\n"
        
        # Show top features
        top_features = sorted(features, key=lambda x: x.scientific_interest, reverse=True)[:3]
        for feature in top_features:
            yield f"**{feature.feature_type.replace('_', ' ').title()}** ({feature.feature_id})\n"
            yield f"- Location: {feature.location[0]:.3f}°, {feature.location[1]:.3f}°\n"
            yield f"- Scientific Interest: {feature.scientific_interest:.1f}/10\n"
            yield f"- Accessibility: {feature.accessibility.title()}\n"
            yield f"- Composition: {feature.composition.replace('_', ' ')}\n\n"
        
        yield "### Detailed Terrain Analysis\n"
        yield terrain_analysis + "\n\n"
        
        yield "## 🎯 Target Prioritization...\n\n"
        
        # Prioritize targets
        targets, prioritization_analysis = await self.prioritize_targets(features, mission_objectives)
        high_priority = [t for t in targets if t.priority == "high"]
        
        yield f"### Exploration Targets Generated: {len(targets)}\n"
        yield f"- **High Priority:** {len(high_priority)}\n"
        yield f"- **Medium Priority:** {len([t for t in targets if t.priority == 'medium'])}\n"
        yield f"- **Low Priority:** {len([t for t in targets if t.priority == 'low'])}\n\n"
        
        yield "### High Priority Targets\n"
        for target in high_priority[:3]:
            yield f"**{target.target_id}** - {target.target_type.replace('_', ' ').title()}\n"
            yield f"- Coordinates: {target.coordinates[0]:.3f}°, {target.coordinates[1]:.3f}°\n"
            yield f"- Duration: {target.estimated_duration:.1f} sols\n"
            yield f"- Instruments: {', '.join(target.required_instruments)}\n\n"
        
        yield "## 🛰️ Path Planning...\n\n"
        
        # Plan rover path
        rover_position = (0.0, 0.0)  # Starting position
        path_plan, path_analysis = await self.plan_rover_path(targets, rover_position)
        
        yield f"### Optimal Path Generated\n"
        yield f"- **Path ID:** {path_plan.path_id}\n"
        yield f"- **Total Distance:** {path_plan.total_distance:.0f} meters\n"
        yield f"- **Estimated Time:** {path_plan.estimated_time:.1f} sols\n"
        yield f"- **Energy Required:** {path_plan.energy_required:.0f} Wh\n"
        yield f"- **Waypoints:** {len(path_plan.waypoints)}\n"
        yield f"- **Alternative Paths:** {path_plan.alternative_paths}\n\n"
        
        yield "### Path Analysis\n"
        yield path_analysis + "\n\n"
        
        yield "## 🤖 Autonomous Science Planning...\n\n"
        
        # Autonomous science selection
        available_time = 10.0  # sols available for science
        science_plan = await self.autonomous_science_selection(available_time, targets)
        
        yield f"### Autonomous Science Selection\n"
        yield f"- **Time Available:** {available_time} sols\n"
        yield f"- **Targets Selected:** {len(science_plan['selected_targets'])}\n"
        yield f"- **Total Duration:** {science_plan['total_duration']:.1f} sols\n"
        yield f"- **Time Utilization:** {science_plan['utilization']:.1f}%\n\n"
        
        yield "### Selected Science Activities\n"
        for target in science_plan['selected_targets']:
            yield f"- **{target.target_id}:** {target.target_type} ({target.estimated_duration:.1f} sols)\n"
        yield "\n"
        
        yield "### Science Planning Analysis\n"
        yield science_plan['analysis'] + "\n\n"
        
        yield "## 📊 Mission Summary\n\n"
        yield f"- **Terrain Features Analyzed:** {len(features)}\n"
        yield f"- **Exploration Targets:** {len(targets)}\n"
        yield f"- **High Priority Targets:** {len(high_priority)}\n"
        yield f"- **Path Distance:** {path_plan.total_distance:.0f} m\n"
        yield f"- **Science Activities:** {len(science_plan['selected_targets'])}\n"
        yield f"- **Mission Efficiency:** {science_plan['utilization']:.1f}%\n\n"
        
        yield f"---\n**Mission Status: READY FOR EXECUTION** ✅\n"
        yield f"**Next Phase: Surface Operations Commencement**"

# Gradio Interface
async def run_planetary_exploration(planetary_body: str, region: str, objectives: str):
    """Run planetary exploration mission simulation"""
    explorer = NASAPlanetaryExplorer()
    
    # Parse objectives
    mission_objectives = [obj.strip() for obj in objectives.split(',') if obj.strip()]
    if not mission_objectives:
        mission_objectives = ["Search for signs of past life", "Analyze geological composition", "Map surface features"]
    
    async for chunk in explorer.run_exploration_mission(planetary_body, region, mission_objectives):
        yield chunk

# Create Gradio interface
with gr.Blocks(
    title="NASA Planetary Exploration",
    theme=gr.themes.Base(
        primary_hue="amber",
        secondary_hue="red"
    ).set(
        body_background_fill="linear-gradient(45deg, #2a1810, #4a2818)",
        panel_background_fill="rgba(255,255,255,0.05)"
    )
) as demo:
    
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #ffffff; font-size: 2.5em; margin-bottom: 10px;">
            🌍 NASA Planetary Exploration
        </h1>
        <p style="color: #cccccc; font-size: 1.2em;">
            Advanced AI System for Planetary Surface Analysis and Exploration Planning
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            body_dropdown = gr.Dropdown(
                label="Planetary Body",
                choices=[
                    ("Mars", "mars"),
                    ("Moon (Luna)", "moon"),
                    ("Europa (Jupiter's moon)", "europa")
                ],
                value="mars"
            )
            
            region_input = gr.Textbox(
                label="Target Region",
                placeholder="e.g., 'Jezero Crater floor with ancient river delta', 'Mare Imbrium with fresh impact craters', 'Europa's chaos terrain near thermal anomalies'",
                lines=3
            )
            
            objectives_input = gr.Textbox(
                label="Mission Objectives (comma-separated)",
                placeholder="e.g., Search for biosignatures, Analyze mineral composition, Map surface topology, Study water ice deposits",
                lines=2
            )
            
            explore_button = gr.Button(
                "🌍 Start Planetary Exploration",
                variant="primary",
                size="lg"
            )
            
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ffffff;">Exploration Capabilities</h3>
                <ul style="color: #cccccc;">
                    <li>🔍 Autonomous Terrain Analysis</li>
                    <li>🎯 Target Prioritization</li>
                    <li>🛰️ Path Planning & Navigation</li>
                    <li>🤖 Autonomous Science Selection</li>
                    <li>📊 Mission Optimization</li>
                </ul>
                <h4 style="color: #ffffff; margin-top: 20px;">Planetary Bodies</h4>
                <ul style="color: #cccccc; font-size: 0.9em;">
                    <li>🔴 Mars: Active rovers, past water</li>
                    <li>🌙 Moon: Artemis program, ice deposits</li>
                    <li>🌊 Europa: Subsurface ocean, astrobiology</li>
                </ul>
            </div>
            """)
    
    exploration_output = gr.Markdown(
        label="Planetary Exploration Mission",
        value="Planetary exploration system ready. Select target body and region above.",
        container=True
    )
    
    # Event handlers
    explore_button.click(
        fn=run_planetary_exploration,
        inputs=[body_dropdown, region_input, objectives_input],
        outputs=exploration_output
    )
    
    region_input.submit(
        fn=run_planetary_exploration,
        inputs=[body_dropdown, region_input, objectives_input],
        outputs=exploration_output
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7865,
        share=True,
        inbrowser=True
    )