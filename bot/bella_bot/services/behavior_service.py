import json
import os
from typing import Dict, List, Optional

class BehaviorService:
    def __init__(self, file_path="behaviors.json"):
        self.file_path = file_path
        self.data = {
            "personas": {},
            "assignments": {"users": {}, "roles": {}},
            "default_persona": "default",
            "global_guidelines": ""
        }
        self.load()

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    # Migration from old list format to new Controller format
                    if "behaviors" in content and isinstance(content["behaviors"], list):
                        self.migrate_legacy(content["behaviors"])
                    else:
                        self.data = content
            except Exception:
                # If file is corrupt, backup and start fresh? Or just start fresh.
                print("Error loading behaviors.json, starting fresh.")
        else:
            self.save()

    def migrate_legacy(self, old_behaviors):
        # Convert old 3-slot system to new format
        print("Migrating legacy behaviors...")
        self.data["personas"] = {
            "devoted": {
                "name": "Devoted (Owner)", 
                "prompt": old_behaviors[0] if len(old_behaviors) > 0 else "You are devoted and loving."
            },
            "normal": {
                "name": "Normal Bella", 
                "prompt": old_behaviors[1] if len(old_behaviors) > 1 else "You are Bella, confident and bold."
            },
            "savage": {
                "name": "Savage Mode", 
                "prompt": old_behaviors[2] if len(old_behaviors) > 2 else "You are Savage."
            }
        }
        self.data["assignments"]["roles"] = {"Owner": "devoted", "Admin": "devoted"}
        self.data["default_persona"] = "normal"
        # The savage rule was usually a condition, we can add it to global or keep it as a persona.
        # Since the user wants "Choosing", "Savage" might be a persona assigned to "Banned" people?
        # Or better, we put the conditional savage logic into the global guidelines if it applies to everyone.
        # For now, we just migrate the text.
        self.data["global_guidelines"] = "When someone disrespects you, act according to your persona's guidelines for conflict."
        self.save()

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_full_config(self):
        return self.data

    # --- Personas ---
    def update_persona(self, id: str, name: str, prompt: str):
        self.data["personas"][id] = {"name": name, "prompt": prompt}
        self.save()

    def delete_persona(self, id: str):
        if id in self.data["personas"]:
            del self.data["personas"][id]
            # Cleanup assignments
            # (In a real app, we'd remove refs, but lazy is fine for now)
            self.save()

    # --- Assignments ---
    def assign_user(self, user_id: str, persona_id: str):
        if not persona_id:
            if user_id in self.data["assignments"]["users"]:
                del self.data["assignments"]["users"][user_id]
        else:
            self.data["assignments"]["users"][user_id] = persona_id
        self.save()

    def assign_role(self, role_name: str, persona_id: str):
        if not persona_id:
            if role_name in self.data["assignments"]["roles"]:
                del self.data["assignments"]["roles"][role_name]
        else:
            self.data["assignments"]["roles"][role_name] = persona_id
        self.save()
        
    def set_default_persona(self, persona_id: str):
        self.data["default_persona"] = persona_id
        self.save()

    def set_global_guidelines(self, text: str):
        self.data["global_guidelines"] = text
        self.save()

    # --- Resolution ---
    def resolve_system_instruction(self, user_id: str, user_roles: List[str]) -> str:
        """Determines the final system prompt for a specific user interaction"""
        personas = self.data["personas"]
        assignments = self.data["assignments"]
        
        # 1. Check User Assignment
        pid = assignments["users"].get(user_id)
        
        # 2. Check Role Assignment
        if not pid:
            # Check if any user role matches an assigned role
            # Priority: defined by order in assignments? Or arbitrary.
            # We check roles present in 'assignments'
            for role in user_roles:
                if role in assignments["roles"]:
                    pid = assignments["roles"][role]
                    break
        
        # 3. Default
        if not pid:
            pid = self.data.get("default_persona")
            
        # Retrieve Prompt
        persona = personas.get(pid, {})
        persona_prompt = persona.get("prompt", "")
        
        # Combine with Global Guidelines
        guidelines = self.data.get("global_guidelines", "")
        
        return f"{persona_prompt}\n\n{guidelines}"
