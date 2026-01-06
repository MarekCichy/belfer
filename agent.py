import sys
import os

# Dodaje katalog, w którym uruchomiono skrypt, do ścieżki systemowej.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from exam_agent_memory import ExamAgentMemory
import json

# Ustawienie domyślnego ID dla celów testowych
DEFAULT_STUDENT_ID = "student_janka_c"


# --- A. FUNKCJA WCZYTYWANIA PAMIĘCI (BEFORE CALLBACK) ---
# Używamy *args i **kwargs dla elastyczności, rozwiązując błąd 'missing 1 required positional argument'
def load_and_inject_memory(callback_context):
    """
    Wczytuje pamięć studenta i WSTRZYKUJE JĄ BEZPOŚREDNIO do instrukcji Agenta.
    """
    # print(dir(callback_context))
    # print(vars(callback_context))

    # Bezpieczne pobranie obiektu kontekstu
    context = callback_context
    if not context:
        print("[System Error] Brak obiektu 'context' w wywołaniu callback load_and_inject_memory.")
        return None

    student_id = DEFAULT_STUDENT_ID
    memory_manager = ExamAgentMemory(student_id=student_id)
    student_context = memory_manager.get_context_for_agent()

    # Zapisujemy managera i treść pamięci do stanu sesji (dla after_callback)
    context.state['memory_manager'] = memory_manager
    context.state['memory_content'] = student_context  # Nadal przechowujemy to w stanie na wszelki wypadek

    # KLUCZOWA ZMIANA: BEZPOŚREDNIE WSTRZYKNIĘCIE PAMIĘCI DO INSTRUKCJI
    original_instruction = context._invocation_context.agent.instruction  # Pobierz bieżącą instrukcję

    # Wstawiamy wczytany kontekst w placeholder, rozwiązując błąd braku zmiennej
    updated_instruction = original_instruction.replace(
        "[[CONTEXT_PLACEHOLDER]]",
        student_context
    )

    # Nadpisujemy instrukcję Agenta w kontekście
    context._invocation_context.agent.instruction = updated_instruction

    print(f"[System] Pamięć dla {student_id} wczytana i wstrzyknięta do instrukcji.")
    return None

# def load_and_inject_memory(callback_context):
#     print('before_callback_succesful', callback_context)


# --- B. FUNKCJA ZAPISYWANIA PAMIĘCI (AFTER CALLBACK) ---
# Używamy *args i **kwargs dla elastyczności
def summarize_and_save_memory(*args, **kwargs):
    """
    Uruchamia się PO wykonaniu agenta.
    """
    if args:
        context = args[0]
    else:
        context = kwargs.get('context')
        if not context:
            return None

    memory_manager = context.state.get('memory_manager')

    if memory_manager:
        agent_response = context.final_output

        # Symulacja zapisu:
        last_msg = str(agent_response)
        memory_manager.data['last_session_summary'] = f"Ostatnia odp: {last_msg[:50]}..."
        memory_manager.save_memory()

        print("[System] Pamięć zaktualizowana i zapisana.")

    return None


maths_teacher = Agent(
    name="maths_teacher",
    model="gemini-2.0-flash",
    description=(
        "Agent uczący matematyki"
    ),
    instruction=(
        """Jesteś nauczycielem matematyki. Wyjaśniaj pojęcia i pomóż uczniowi rozwiązywać zadania matematyczne.
        Używaj LaTeX do wzorów."""
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
        --- PAMIĘĆ O UCZNIU --- 
        [[CONTEXT_PLACEHOLDER]] 

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
        - Jeśli uczeń pyta o słówka, tłumaczenie, gramatykę obcą -> Uruchom: [language_teacher]
        - Jeśli uczeń chce zaplanować naukę lub mówi, że jest zmęczony -> Obsłuż to samodzielnie, proponując przerwę lub tworząc plan.

        PAMIĘĆ I KONTEKST:
        - Korzystaj z historii rozmowy. Jeśli uczeń wraca do tematu, który sprawiał trudność, przypomnij o tym delikatnie ("Pamiętam, że ostatnio walczyliśmy z ułamkami, sprawdzimy to?")."""
    ),
    sub_agents=[maths_teacher, polish_teacher, language_teacher],
    before_agent_callback=[load_and_inject_memory],
    after_agent_callback=[summarize_and_save_memory]
)