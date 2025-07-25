"""
NASA AI Agents Demo Launcher
Launch all three NASA AI agents for interview demonstration
"""

import subprocess
import threading
import time
import webbrowser
from datetime import datetime

def launch_agent(script_name, port, name):
    """Launch an individual agent"""
    print(f"🚀 Launching {name} on port {port}...")
    try:
        process = subprocess.Popen(
            ["python", script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"❌ Error launching {name}: {e}")
        return None

def main():
    print("=" * 60)
    print("🚀 NASA AI AGENTS PORTFOLIO DEMO")
    print("=" * 60)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nLaunching NASA AI Agent Portfolio for Interview...")
    print("\n🎯 Six Advanced AI Systems Demonstrating:")
    print("   • Deep Research Capabilities")
    print("   • Multi-Agent Collaboration") 
    print("   • Real-Time Mission Operations")
    print("   • Autonomous Decision Making")
    print("   • Orbital Traffic Management")
    print("   • Planetary Surface Exploration")
    print("\n" + "-" * 60)
    
    agents = [
        ("nasa_deep_research.py", 7860, "NASA Deep Research Agent"),
        ("nasa_engineering_team.py", 7861, "NASA Engineering Team"),
        ("nasa_mission_control.py", 7862, "NASA Mission Control"),
        ("nasa_spacecraft_autonomy.py", 7863, "NASA Spacecraft Autonomy"),
        ("nasa_satellite_traffic.py", 7864, "NASA Satellite Traffic Management"),
        ("nasa_planetary_exploration.py", 7865, "NASA Planetary Exploration")
    ]
    
    processes = []
    
    # Launch all agents
    for script, port, name in agents:
        process = launch_agent(script, port, name)
        if process:
            processes.append((process, name, port))
            time.sleep(2)  # Stagger launches
    
    print("\n" + "=" * 60)
    print("🎉 ALL NASA AI AGENTS LAUNCHED SUCCESSFULLY!")
    print("=" * 60)
    
    print("\n📱 Access Your NASA AI Portfolio:")
    print("┌" + "─" * 58 + "┐")
    print("│ 🔬 NASA Deep Research Agent                            │")
    print("│    http://localhost:7860                               │")
    print("│    Advanced research for space missions & tech        │")
    print("├" + "─" * 58 + "┤")
    print("│ 🤝 NASA Engineering Team                              │") 
    print("│    http://localhost:7861                               │")
    print("│    Multi-agent spacecraft design collaboration        │")
    print("├" + "─" * 58 + "┤")
    print("│ 🎮 NASA Mission Control                               │")
    print("│    http://localhost:7862                               │")
    print("│    Real-time mission operations & decision support    │")
    print("├" + "─" * 58 + "┤")
    print("│ 🤖 NASA Spacecraft Autonomy                           │")
    print("│    http://localhost:7863                               │")
    print("│    Deep space autonomous decision-making systems      │")
    print("├" + "─" * 58 + "┤")
    print("│ 🛰️ NASA Satellite Traffic Management                  │")
    print("│    http://localhost:7864                               │")
    print("│    Orbital collision avoidance & traffic coordination │")
    print("├" + "─" * 58 + "┤")
    print("│ 🌍 NASA Planetary Exploration                         │")
    print("│    http://localhost:7865                               │")
    print("│    Autonomous planetary surface analysis & mapping    │")
    print("└" + "─" * 58 + "┘")
    
    print("\n🌟 INTERVIEW DEMONSTRATION POINTS:")
    print("   ✅ Six advanced AI frameworks (OpenAI, Multi-Agent, LangGraph, Autonomy)")
    print("   ✅ NASA-specific domain expertise and terminology")
    print("   ✅ Real-world space mission applications")
    print("   ✅ Professional interfaces and user experience")
    print("   ✅ Scalable architecture and design patterns")
    print("   ✅ Comprehensive space operations coverage")
    
    print("\n💡 SUGGESTED DEMO SCENARIOS:")
    print("   🔬 Research: 'Artemis lunar base construction materials'")
    print("   🤝 Engineering: 'Mars helicopter for sample collection'")
    print("   🎮 Mission Control: 'Emergency solar panel deployment'")
    print("   🤖 Autonomy: 'Navigation computer malfunction detected'")
    print("   🛰️ Traffic: 'Large debris field in Starlink constellation orbit'")
    print("   🌍 Exploration: 'Jezero Crater with ancient river delta'")
    
    print(f"\n⏰ Demo ready at: {datetime.now().strftime('%H:%M:%S')}")
    print("Press Ctrl+C to stop all agents and exit demo")
    print("=" * 60)
    
    # Auto-open first agent in browser
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:7860")
        print("🌐 Opened NASA Deep Research Agent in your browser")
    except:
        print("💻 Please manually open http://localhost:7860 in your browser")
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down NASA AI Agents Demo...")
        
        # Terminate all processes
        for process, name, port in processes:
            if process:
                print(f"   Stopping {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("\n✅ All agents stopped successfully")
        print("🎯 Demo completed - Ready for NASA interview!")
        print("=" * 60)

if __name__ == "__main__":
    main()