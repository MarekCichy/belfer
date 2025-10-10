import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def retrieve_course(login: str) -> dict:
    """Retrieves data about the course and last lesson for a given login.

    Args:
        login (str): The login associated with a given course

    Returns:
        course: json with course plan
        last_lesson: last lesson interactions
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


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