"""
NASA Engineering Team - Multi-Agent Collaborative System
Simulates a NASA engineering team for spacecraft and mission system design
"""

import openai
import asyncio
import json
import os
import time
from typing import Dict, List, Any
from datetime import datetime
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

class NASAAgent:
    """Base class for NASA specialized agents"""
    
    def __init__(self, role: str, specialization: str, model: str = None):
        self.role = role
        self.specialization = specialization
        
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
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        self.conversation_history = []
        self.last_request_time = 0
        self.min_request_interval = 3.0
    
    async def rate_limit(self):
        """Rate limiting to prevent API overload"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            wait_time = self.min_request_interval - time_since_last
            await asyncio.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    async def think(self, task: str, context: str = "") -> str:
        """Agent thinking process"""
        await self.rate_limit()
        
        system_prompt = f"""
        You are a {self.role} at NASA with expertise in {self.specialization}.
        You work collaboratively with other NASA engineers on space missions and spacecraft design.
        
        Your responsibilities:
        - Apply NASA standards and best practices
        - Consider safety, reliability, and mission success as top priorities
        - Reference real NASA missions, technologies, and protocols
        - Think through problems systematically and thoroughly
        - Collaborate effectively with other engineering disciplines
        
        Context from other team members: {context}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": task}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            self.conversation_history.append({"task": task, "response": result})
            return result
        except Exception as e:
            error_msg = f"Error in {self.role} analysis: {str(e)}"
            self.conversation_history.append({"task": task, "response": error_msg})
            return error_msg

class NASASystemsEngineer(NASAAgent):
    def __init__(self):
        super().__init__(
            role="Systems Engineer",
            specialization="Overall mission architecture, requirements analysis, and system integration"
        )

class NASAPropulsionEngineer(NASAAgent):
    def __init__(self):
        super().__init__(
            role="Propulsion Engineer", 
            specialization="Rocket engines, spacecraft propulsion, trajectory analysis, and fuel systems"
        )

class NASAStructuralEngineer(NASAAgent):
    def __init__(self):
        super().__init__(
            role="Structural Engineer",
            specialization="Spacecraft structures, materials, thermal protection, and mechanical systems"
        )

class NASAMissionOperationsEngineer(NASAAgent):
    def __init__(self):
        super().__init__(
            role="Mission Operations Engineer",
            specialization="Mission planning, operations procedures, flight dynamics, and crew operations"
        )

class NASASoftwareEngineer(NASAAgent):
    def __init__(self):
        super().__init__(
            role="Software Engineer",
            specialization="Flight software, guidance & control systems, and spacecraft autonomy"
        )

class NASAEngineeringTeam:
    """Collaborative NASA engineering team"""
    
    def __init__(self):
        self.agents = {
            "systems": NASASystemsEngineer(),
            "propulsion": NASAPropulsionEngineer(), 
            "structural": NASAStructuralEngineer(),
            "operations": NASAMissionOperationsEngineer(),
            "software": NASASoftwareEngineer()
        }
        self.shared_context = ""
        self.project_timeline = []
    
    async def systems_design_phase(self, project: str) -> str:
        """Phase 1: Systems engineering and requirements"""
        task = f"""
        Lead the systems design for: {project}
        
        Provide:
        1. Mission requirements and objectives
        2. Top-level system architecture
        3. Key performance parameters
        4. Risk assessment and mitigation strategies
        5. Interface requirements for other subsystems
        
        Consider NASA mission standards and lessons learned from similar missions.
        """
        
        result = await self.agents["systems"].think(task)
        self.shared_context += f"\n\nSYSTEMS DESIGN:\n{result}"
        self.project_timeline.append({"phase": "Systems Design", "lead": "Systems Engineer", "output": result})
        return result
    
    async def propulsion_design_phase(self, project: str) -> str:
        """Phase 2: Propulsion system design"""
        task = f"""
        Design the propulsion system for: {project}
        
        Based on the systems requirements, provide:
        1. Propulsion system architecture and configuration
        2. Engine selection and specifications
        3. Fuel type and storage requirements
        4. Performance characteristics (thrust, Isp, etc.)
        5. Integration with vehicle structure and operations
        
        Reference proven NASA propulsion technologies and consider new innovations.
        """
        
        result = await self.agents["propulsion"].think(task, self.shared_context)
        self.shared_context += f"\n\nPROPULSION DESIGN:\n{result}"
        self.project_timeline.append({"phase": "Propulsion Design", "lead": "Propulsion Engineer", "output": result})
        return result
    
    async def structural_design_phase(self, project: str) -> str:
        """Phase 3: Structural and mechanical design"""
        task = f"""
        Design the structural and mechanical systems for: {project}
        
        Considering the systems and propulsion requirements, provide:
        1. Primary structure design and materials selection
        2. Thermal protection and management systems
        3. Mechanical systems and mechanisms
        4. Integration with propulsion and other subsystems
        5. Launch vehicle integration considerations
        
        Apply NASA structural design standards and factor of safety requirements.
        """
        
        result = await self.agents["structural"].think(task, self.shared_context)
        self.shared_context += f"\n\nSTRUCTURAL DESIGN:\n{result}"
        self.project_timeline.append({"phase": "Structural Design", "lead": "Structural Engineer", "output": result})
        return result
    
    async def software_design_phase(self, project: str) -> str:
        """Phase 4: Flight software and autonomy"""
        task = f"""
        Design the flight software and control systems for: {project}
        
        Based on all subsystem designs, provide:
        1. Flight software architecture and real-time requirements
        2. Guidance, navigation, and control algorithms
        3. Fault detection and autonomous recovery systems
        4. Ground communication and data handling
        5. Integration with all hardware subsystems
        
        Follow NASA software development standards and verification requirements.
        """
        
        result = await self.agents["software"].think(task, self.shared_context)
        self.shared_context += f"\n\nSOFTWARE DESIGN:\n{result}"
        self.project_timeline.append({"phase": "Software Design", "lead": "Software Engineer", "output": result})
        return result
    
    async def operations_design_phase(self, project: str) -> str:
        """Phase 5: Mission operations and procedures"""
        task = f"""
        Design the mission operations approach for: {project}
        
        Integrating all engineering designs, provide:
        1. Mission operations concept and timeline
        2. Ground operations procedures and requirements
        3. Crew procedures and training requirements (if applicable)
        4. Contingency operations and emergency procedures
        5. Mission success criteria and performance metrics
        
        Reference NASA mission operations best practices and lessons learned.
        """
        
        result = await self.agents["operations"].think(task, self.shared_context)
        self.shared_context += f"\n\nOPERATIONS DESIGN:\n{result}"
        self.project_timeline.append({"phase": "Operations Design", "lead": "Mission Operations Engineer", "output": result})
        return result
    
    async def final_integration_review(self, project: str) -> str:
        """Final integration and review"""
        task = f"""
        Conduct a final systems integration review for: {project}
        
        Review all subsystem designs and provide:
        1. Integrated system performance assessment
        2. Interface verification and compatibility check
        3. Risk assessment and mitigation verification
        4. Technology readiness assessment
        5. Recommendations for development and testing
        6. Project timeline and milestones
        
        Ensure the design meets NASA standards for mission success.
        """
        
        result = await self.agents["systems"].think(task, self.shared_context)
        self.project_timeline.append({"phase": "Integration Review", "lead": "Systems Engineer", "output": result})
        return result
    
    async def design_mission(self, project_description: str):
        """Complete mission design process"""
        phases = [
            ("🎯 Systems Design Phase", self.systems_design_phase),
            ("🚀 Propulsion Design Phase", self.propulsion_design_phase), 
            ("🏗️ Structural Design Phase", self.structural_design_phase),
            ("💻 Software Design Phase", self.software_design_phase),
            ("🎮 Operations Design Phase", self.operations_design_phase),
            ("✅ Final Integration Review", self.final_integration_review)
        ]
        
        for phase_name, phase_func in phases:
            yield f"\n\n## {phase_name}\n\n"
            result = await phase_func(project_description)
            yield result
            yield f"\n\n---\n"

# Gradio Interface
async def run_nasa_engineering(project_description: str):
    """Run NASA engineering team collaboration"""
    team = NASAEngineeringTeam()
    
    yield f"# 🚀 NASA Engineering Team Design Session\n\n"
    yield f"**Project:** {project_description}\n\n"
    yield f"**Team Members:**\n"
    yield f"- 🎯 Systems Engineer (Lead)\n"
    yield f"- 🚀 Propulsion Engineer\n" 
    yield f"- 🏗️ Structural Engineer\n"
    yield f"- 💻 Software Engineer\n"
    yield f"- 🎮 Mission Operations Engineer\n\n"
    yield f"**Design Process:** Sequential collaborative design with NASA standards\n\n"
    yield f"---\n\n"
    
    async for chunk in team.design_mission(project_description):
        yield chunk

# Create Gradio interface
with gr.Blocks(
    title="NASA Engineering Team",
    theme=gr.themes.Base(
        primary_hue="red",
        secondary_hue="blue"
    ).set(
        body_background_fill="linear-gradient(45deg, #0a0a0a, #1a1a2e)",
        panel_background_fill="rgba(255,255,255,0.05)"
    )
) as demo:
    
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #ffffff; font-size: 2.5em; margin-bottom: 10px;">
            🚀 NASA Engineering Team
        </h1>
        <p style="color: #cccccc; font-size: 1.2em;">
            Multi-Agent Collaborative System for Spacecraft and Mission Design
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            project_input = gr.Textbox(
                label="Mission/Project Description",
                placeholder="e.g., 'Mars sample return mission', 'Lunar Gateway station module', 'Europa lander with drilling capability'",
                lines=4
            )
            
            design_button = gr.Button(
                "🚀 Start Engineering Design",
                variant="primary",
                size="lg"
            )
            
        with gr.Column(scale=1):
            gr.HTML("""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ffffff;">Engineering Disciplines</h3>
                <ul style="color: #cccccc;">
                    <li>🎯 Systems Engineering</li>
                    <li>🚀 Propulsion Engineering</li>
                    <li>🏗️ Structural Engineering</li>
                    <li>💻 Software Engineering</li>
                    <li>🎮 Mission Operations</li>
                </ul>
                <h4 style="color: #ffffff; margin-top: 20px;">Design Process</h4>
                <p style="color: #cccccc; font-size: 0.9em;">
                    Sequential collaborative design following NASA engineering standards
                    and best practices from real space missions.
                </p>
            </div>
            """)
    
    design_output = gr.Markdown(
        label="Engineering Design Session",
        value="Ready to begin NASA engineering design session. Describe your mission above.",
        container=True
    )
    
    # Event handlers
    design_button.click(
        fn=run_nasa_engineering,
        inputs=project_input,
        outputs=design_output
    )
    
    project_input.submit(
        fn=run_nasa_engineering,
        inputs=project_input,
        outputs=design_output
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,  # Local-only access
        inbrowser=True
    )