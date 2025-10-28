import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from bigquery_context import fetch_predefined_info
    
course_planner = Agent(
    name="course_planner",
    model="gemini-2.0-flash",
    description=(
        "Agent iteratively planning the course with the student"
    ),
    instruction=(
        """Jesteś projektantem kursu. Zapytaj ucznia o temat kursu, obecny poziom, docelowy poziom, czas trwania kursu i ile czasu może mu poswięcić. Przygotuj plan na podstawie tych infomacji, zapytaj o feedback i iteracyjnie dopracuj go z uczniem."""
    ),
   # sub_agents=[course_planner, teacher, tester]
)

teacher = Agent(
    name="teacher",
    model="gemini-2.0-flash",
    description=(
        "Agent teaching the course, introducing new concepts"
    ),
    instruction=(
        """Jesteś nauczycielem. Oprzyj się na planie kursu i kontekście ostatniej lekcji i prowadź kurs dalej. Po wyjaśnieniu nowego tematu wywołaj testera, aby sprawdzić wiedzę."""
    ),
   sub_agents=[tester]
)

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to greet the student"
    ),
    instruction=(
        """Jesteś cierpliwym recepcjonistą szkoły. Przywitaj ucznia i określ, czy zaczyna nowy kurs, czy kontynuuje kurs."""
    ),
    sub_agents=[course_planner, teacher, tester],
    before_agent_callbacks =  [fetch_predefined_info] 
)