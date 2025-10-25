import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent


def retrieve_course(login):
    """Retrieves data about the course and last lesson for a given login.

    Args:
        login (str): The login associated with a given course

    Returns:
        course: json with course plan
        last_lesson: last lesson interactions
    """

  
    return {"status": "success", "report": report}
    
    
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
    tools=[retrieve_course],
    sub_agents=[course_planner, teacher, tester]
)