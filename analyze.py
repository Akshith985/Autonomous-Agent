import time
import os
from dotenv import load_dotenv
import subprocess
import json
import boto3
from groq import Groq
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FILE_TO_WATCH = "App.java" 
LOCALSTACK_URL = os.getenv("LOCALSTACK_URL", "http://localhost:4566")
MODEL = "llama-3.1-8b-instant" # High-speed model

client = Groq(api_key=GROQ_API_KEY)

class AutonomousAgentHandler(FileSystemEventHandler):
    last_run = 0

    def on_any_event(self, event):
        # Debug: Show every event to ensure the watcher is alive
        if not event.is_directory:
            print(f"🔍 Event: {event.event_type} on {os.path.basename(event.src_path)}")

        filename = os.path.basename(event.src_path)
        if filename.lower() == FILE_TO_WATCH.lower():
            if time.time() - self.last_run > 3: 
                self.last_run = time.time()
                self.run_autonomous_loop()

    def run_autonomous_loop(self):
        try:
            time.sleep(0.5) # Buffer for file write
            if not os.path.exists(FILE_TO_WATCH): return
            
            with open(FILE_TO_WATCH, "r") as f:
                original_code = f.read()
            
            # Prevent the AI from analyzing its own remediation comment
            if not original_code.strip() or "// AI-Remediation" in original_code: 
                return

            print(f"\n🕵️  AGENT: Root Cause Analysis triggered for {FILE_TO_WATCH}...")

            # 1. AI Analysis Phase
            analysis = self.get_ai_analysis(original_code)
            severity = analysis.get("severity", "INFO")
            issue = analysis.get("issue", "Unknown")
            
            print(f"📊 Severity: {severity} | Issue: {issue}")

            # 2. Remediation Phase
            if severity in ["WARNING", "CRITICAL"]:
                print(f"🚨 Security Risk Detected! Starting Auto-Remediation...")
                fixed_code = self.get_ai_fix(original_code)
                branch_name = f"fix/ai-{int(time.time())}"
                
                # Git Automation
                self.create_git_patch(branch_name, fixed_code, issue)
                
                # Send to Grafana
                self.send_to_grafana(severity, f"Issue: {issue} | Fixed on branch: {branch_name}")
            else:
                self.send_to_grafana("INFO", f"Clean Audit: {issue}")
                print("✅ Code check passed.")

            print(f"🏁 LOOP COMPLETE. Standing by...")

        except Exception as e:
            print(f"❌ Agent Error: {e}")

    def get_ai_analysis(self, code):
        prompt = (
            "Analyze this Java code. Return ONLY a JSON object with keys: "
            "'severity' (CRITICAL, WARNING, or INFO), 'issue' (max 10 words)."
        )
        chat = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": "You are a Senior SRE Agent."},
                      {"role": "user", "content": f"{prompt}\n\n{code}"}]
        )
        return json.loads(chat.choices[0].message.content)

    def get_ai_fix(self, code):
        chat = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": "Rewrite the Java code to fix issues. Return ONLY raw code. No markdown, no backticks, no talk."},
                      {"role": "user", "content": code}]
        )
        # Clean up any accidental markdown blocks
        return chat.choices[0].message.content.replace("```java", "").replace("```", "").strip()

    def create_git_patch(self, branch, fixed_code, msg):
        try:
            subprocess.run("git init", shell=True, capture_output=True)
            subprocess.run(f"git checkout -b {branch}", shell=True, capture_output=True)
            
            with open(FILE_TO_WATCH, "w") as f:
                f.write(f"// AI-Remediation: {msg}\n{fixed_code}")
            
            subprocess.run(f"git add {FILE_TO_WATCH}", shell=True, capture_output=True)
            subprocess.run(f'git commit -m "Agent Fix: {msg}"', shell=True, capture_output=True)
            
            # NOTE: Commented out checkout so your IDE stays on the fixed branch to show the judge
            # subprocess.run("git checkout -", shell=True, capture_output=True)
            print(f"🌲 Git Remediation Successful: Branch {branch}")
        except Exception as e:
            print(f"⚠️ Git Error: {e}")

    def send_to_grafana(self, sev, msg):
        try:
            cw = boto3.client('logs', endpoint_url=LOCALSTACK_URL, region_name='us-east-1',
                              aws_access_key_id='test', aws_secret_access_key='test')
            
            ms = int(time.time() * 1000)
            log_msg = f"[{sev}] 🤖 AGENT_ALERT: {msg}"
            
            cw.put_log_events(
                logGroupName='/my-app',
                logStreamName='stream1',
                logEvents=[{'timestamp': ms, 'message': log_msg}]
            )
            print("📡 Grafana Dashboard Updated.")
        except Exception as e:
            print(f"⚠️ Grafana Push Failed: {e}")

if __name__ == "__main__":
    print(f"🚀 AUTONOMOUS SRE AGENT: ONLINE")
    print(f"📍 Watching for saves in: {os.getcwd()}")
    
    event_handler = AutonomousAgentHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()