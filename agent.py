from google.adk import Agent, AgentContext, AgentResponse
from exam_agent_memory import ExamAgentMemory  # Upewnij się, że import jest poprawny
import json

# Ustawienie domyślnego ID dla celów testowych
DEFAULT_STUDENT_ID = "student_janka_c"


# --- A. FUNKCJA WCZYTYWANIA PAMIĘCI (BEFORE CALLBACK) ---
def load_and_inject_memory(context: AgentContext):
    """
    Wczytuje pamięć studenta i wstrzykuje kontekst do instrukcji systemowej Agenta Głównego.

    W ADK kontekst 'context.session_id' lub inne metadane mogą posłużyć jako ID studenta.
    Na razie używamy stałego DEFAULT_STUDENT_ID.
    """

    # 1. Określenie ID studenta (np. na podstawie sesji lub metadanych)
    # W rzeczywistej aplikacji użyłbyś kontekstu (np. context.session_id)
    student_id = DEFAULT_STUDENT_ID

    # 2. Inicjalizacja i wczytanie pamięci
    memory_manager = ExamAgentMemory(student_id=student_id)
    student_context = memory_manager.get_context_for_agent()

    # 3. Wstrzyknięcie pamięci do instrukcji systemowej Agenta
    # Pamiętaj, że instrukcja Agenta Głównego musi być gotowa na przyjęcie kontekstu.

    # Zapisujemy pamięć w metadanych dla późniejszego użycia w after_agent_callbacks
    context.metadata['memory_manager'] = memory_manager

    print(f"\n[DEBUG: CALLBACK INJECT] Wstrzykiwany kontekst:\n{student_context}")

    # Zwracamy kontekst do wstrzyknięcia do instrukcji systemowej
    return f"""
    --- PAMIĘĆ DŁUGOTERMINOWA DLA UCZNIA: {student_id} ---
    {student_context}
    -----------------------------------------------------
    """


# --- B. FUNKCJA ZAPISYWANIA PAMIĘCI (AFTER CALLBACK) ---
def summarize_and_save_memory(context: AgentContext, response: AgentResponse):
    """
    Analizuje odpowiedź Agenta, generuje podsumowanie i zapisuje do pamięci.
    """

    # 1. Odzyskanie Managera Pamięci z metadanych
    if 'memory_manager' not in context.metadata:
        print("Błąd: Memory Manager nie znaleziony w kontekście.")
        return response

    memory_manager: ExamAgentMemory = context.metadata['memory_manager']

    # 2. Analiza i podsumowanie (tutaj musi być logika LLM!)
    # W idealnym świecie, użyłbyś modelu do analizy 'response.history' i wygenerowania nowego JSON-a

    # PRZYKŁADOWA LOGIKA (Symulacja):
    # Prosimy model o podsumowanie i generujemy dane do zapisu:
    if "matematyka" in response.text.lower() and "wzory" in response.text.lower():
        # Aktualizacja słabych punktów, jeśli model stwierdził problem
        memory_manager.update_weaknesses("mathematics", "Problem with formula application")

    # Aktualizacja ostatniej sesji
    memory_manager.data['last_session_summary'] = f"Sesja zakończona. Ostatnia odpowiedź: {response.text[:50]}..."

    # Zapis do pliku
    memory_manager.save_memory()
    print("Pamięć została pomyślnie zaktualizowana i zapisana.")

    return response  # Zwracamy oryginalną odpowiedź

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
    sub_agents=[maths_teacher, polish_teacher, language_teacher],
    before_agent_callbacks=[load_and_inject_memory],
    after_agent_callbacks=[summarize_and_save_memory]
)

