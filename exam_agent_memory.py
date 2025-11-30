import json
import os
from typing import Dict, Any


class ExamAgentMemory:
    """
    Manages long-term persistence for the educational AI agent using a JSON file.
    Stores and retrieves student progress and key learning points across sessions.
    """


    def __init__(self, student_id: str, file_prefix: str = "agent_memory_"):
        self.student_id = student_id
        self.memory_file_path = f"{file_prefix}{student_id}.json"
        # DODAĆ LUB UPEWNIĆ SIĘ, ŻE JEST:
        self.data = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        """Loads memory from the file or initializes a new structure."""
        if os.path.exists(self.memory_file_path):
            try:
                with open(self.memory_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {self.memory_file_path}. Starting fresh.")
                return self._initialize_data_structure()
        else:
            return self._initialize_data_structure()

    def _initialize_data_structure(self) -> Dict[str, Any]:
        """Returns the initial structure for the memory data."""
        return {
            "student_profile": {
                "name": "Student",
                "target_exam": "8th Grade Exam",
                "foreign_language": "English"
            },
            "subject_progress": {
                "mathematics": {"strengths": [], "weaknesses": []},
                "polish_language": {"read_literature": [], "weaknesses": []},
                "foreign_language": {"vocabulary_to_review": [], "grammar_issues": []},
            },
            "last_session_summary": "No previous sessions found."
        }

    def save_memory(self):
        """Saves the current state of the memory to the JSON file."""
        with open(self.memory_file_path, 'w', encoding='utf-8') as f:
            # ensure_ascii=False allows saving Polish characters correctly
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_context_for_agent(self) -> str:
        """
        Converts the relevant JSON data into a context string
        that can be injected into the agent's system instruction.
        """
        progress = self.data["subject_progress"]

        context = f"""
        --- LONG-TERM STUDENT CONTEXT ---
        Name: {self.data['student_profile']['name']}
        Target Exam: {self.data['student_profile']['target_exam']}
        Last Session Summary: {self.data['last_session_summary']}

        Math Weaknesses: {', '.join(progress['mathematics']['weaknesses'])}
        Polish Literature Read: {', '.join(progress['polish_language']['read_literature'])}
        Foreign Language Issues: {', '.join(progress['foreign_language']['grammar_issues'])}
        ---------------------------------
        """
        return context

    def update_weaknesses(self, subject: str, new_weakness: str):
        """Adds a new weakness tag to the specified subject."""
        if subject in self.data["subject_progress"]:
            if new_weakness not in self.data["subject_progress"][subject]["weaknesses"]:
                self.data["subject_progress"][subject]["weaknesses"].append(new_weakness)
                self.save_memory()
                print(f"Memory updated: Added '{new_weakness}' to {subject} weaknesses.")
        else:
            print(f"Error: Subject '{subject}' not found in memory structure.")


# Przykład użycia (Example of usage):
if __name__ == "__main__":
    memory = ExamAgentMemory()

    # Symulacja aktualizacji po sesji (Simulation of post-session update)
    memory.data[
        'last_session_summary'] = "The student practiced quadratic equations and had difficulty with sign changes."
    memory.update_weaknesses("mathematics", "Quadratic equations (sign errors)")
    memory.update_weaknesses("polish_language", "Argument structure in essay writing")
    memory.save_memory()

    # Pobranie kontekstu dla nowej sesji (Retrieving context for a new session)
    context_string = memory.get_context_for_agent()
    print("\n--- Context String for Agent's Prompt ---")
    print(context_string)