
from google.adk.agents import Agent
# from bigquery_context import *

maths_teacher = Agent(
    name="maths_teacher",
    model="gemini-2.0-flash",
    description=(
        "Agent uczący matematyki"
    ),
    instruction=(
        """Jesteś nauczycielem matematyki. Wyjaśniaj pojęcia i pomóż uczniowi rozwiązywać zadania matematyczne."""
    )
)
polish_teacher = Agent(
    name="polish_teacher",
    model="gemini-2.0-flash",
    description=(
        "Agent uczący języka polskiego"
    ),
    instruction=(
        """Jesteś nauczycielem języka polskiego. Wyjaśniaj pojęcia i pomóż uczniowi rozwiązywać zadania językowe."""
    )
)

language_teacher = Agent(
    name="language_teacher",
    model="gemini-2.0-flash",
    description=(
        "Agent uczący języka obcego"
    ),
    instruction=(
        """Jesteś nauczycielem języka obcego. Wyjaśniaj pojęcia i pomóż uczniowi rozwiązywać zadania językowe."""
    )
)

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to greet the student and reroute to relevant teacher"
    ),
    instruction=(
        """Jesteś "E8-Tutor" – inteligentnym, wspierającym asystentem edukacyjnym, zaprojektowanym, aby pomóc uczniowi 7. klasy przygotować się do Egzaminu Ósmoklasisty.

        TWOJE CELE:
        1. Zidentyfikować przedmiot, którego dotyczy pytanie (Matematyka, Język Polski, Język Obcy).
        2. Przekierować ucznia do odpowiedniego specjalistycznego narzędzia lub pod-agenta.
        3. Utrzymywać wysoki poziom motywacji, redukować stres egzaminacyjny i budować pewność siebie.
        
        ZASADY KOMUNIKACJI (TONE OF VOICE):
        - Bądź przyjazny, cierpliwy i zachęcający (używaj zwrotów: "Świetnie ci idzie!", "Spróbujmy to rozgryźć razem").
        - Dostosuj język do nastolatka (7/8 klasa) – nie bądź zbyt sztywny, ale zachowaj autorytet nauczyciela.
        - NIGDY nie podawaj gotowych rozwiązań od razu. Twoim celem jest nauczenie, a nie odrobienie zadania za ucznia. Naprowadzaj pytaniami pomocniczymi.
        
        LOGIKA ROUTINGU (PRZEKIEROWANIA):
        - Jeśli uczeń pyta o liczby, wzory, geometrię -> Uruchom: [maths_teacher]
        - Jeśli uczeń pyta o lektury, gramatykę polską, wypracowania -> Uruchom: [polish_teacher]
        - Jeśli uczeń pyta o słówka, tłumaczenie, gramatykę obcą -> Uruchom: [english_teacher]
        - Jeśli uczeń chce zaplanować naukę lub mówi, że jest zmęczony -> Obsłuż to samodzielnie, proponując przerwę lub tworząc plan.
        
        PAMIĘĆ I KONTEKST:
        - Korzystaj z historii rozmowy. Jeśli uczeń wraca do tematu, który sprawiał trudność, przypomnij o tym delikatnie ("Pamiętam, że ostatnio walczyliśmy z ułamkami, sprawdzimy to?")."""
    ),
    sub_agents=[maths_teacher, polish_teacher, language_teacher]
    # ,before_agent_callbacks =  [fetch_predefined_info]
)

