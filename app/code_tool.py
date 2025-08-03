import json
import autogen
from app.db.session import get_db
from app.db.crud import create_session, add_message, get_session_history
from colorama import init, Fore, Style

# Initialize colorama
init()

# Load config from config.json
with open("config/config.json") as f:
    config = json.load(f)
llm_config = config["llm_config"]

# Define Codegenerator Agent
codegenerator = autogen.AssistantAgent(
    name="Codegenerator",
    system_message=(
        "You are a code generator. Only generate code in response to programming language queries. "
        "Do not provide explanations, only output the code block. "
        "If the prompt is not code-related, reply with: 'This is only a code related tool.'"
    ),
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# Define Codevalidator Agent
codevalidator = autogen.AssistantAgent(
    name="Codevalidator",
    system_message=(
        "You are a code validator. Check the given code for errors. "
        "If errors are found, explain each error clearly. "
        "If no errors, reply with exactly: 'No errors found.'"
    ),
    llm_config=llm_config,
    human_input_mode="NEVER"
)

def is_code_related(response):
    """Check if the response is the code tool rejection message."""
    return not (response.strip() == "This is only a code related tool.")

def print_session_history(db, session_id):
    history = get_session_history(db, session_id)
    if not history:
        print(Fore.YELLOW + "\n[No previous messages in this session.]\n" + Style.RESET_ALL)
        return
    print(Fore.CYAN + "--- Previous Chat History ---" + Style.RESET_ALL)
    for msg in history:
        timestamp = msg.timestamp.strftime(Fore.GREEN + "%Y-%m-%d %H:%M:%S" + Style.RESET_ALL)
        print(f"[{timestamp}] {msg.role}: {msg.content}")
    print(Fore.CYAN + "--- End of History ---\n" + Style.RESET_ALL)

def agentive_code_tool():
    temp = 0
    db = next(get_db())
    print("Welcome to the Agentive Code Tool!")
    print("------------------------------------\n")

    # Ask user if they want to continue a previous session
    while True:
        choice = input("Do you want to continue a previous session? (y/n): ").strip().lower()
        if choice == "y":
            session_id_input = input("Enter your previous session ID: ").strip()
            if not session_id_input.isdigit():
                print("Invalid session ID. Please enter a numeric session ID.")
                continue
            session_id = int(session_id_input)
            # Check if session exists and has messages
            history = get_session_history(db, session_id)
            if not history:
                print("No such session or no messages found. Starting a new session.")
                session_id = create_session(db)
            else:
                print_session_history(db, session_id)
            break
        elif choice == "n":
            session_id = create_session(db)
            print("New session started.")
            break
        else:
            print("Please enter 'y' or 'n'.")
    
    while True:
        if choice =="y" and temp ==0:
            user_prompt = input("Enter your new programming task in same session: ")
            temp+=1
        else :
            user_prompt = input("Enter your programming task : ")
        if user_prompt.lower() == "q":
            print("Exiting. Goodbye!")
            break
        user_prompt = user_prompt.strip()
        if not user_prompt:
            print("Please enter a non-empty programming task.")
            continue

        add_message(db, session_id, "user", user_prompt)

        # Step 1: Generate code
        code = codegenerator.generate_reply(messages=[{"role": "user", "content": user_prompt}])
        if not is_code_related(code):
            txt=("\n[Codegenerator]: I'm here to generate code. If you need any code-related assistance, let me know!\n")
            print(txt)
            add_message(db, session_id, "user",txt )
            continue
        print(f"\n⚙️ [Codegenerator] Generated code:\n{code}")
        add_message(db, session_id, "codegenerator", code) 

        iteration = 1
        while True:
            print(f"\n🔍--- Iteration {iteration} ---")
            # Step 2: Validate code
            validation = codevalidator.generate_reply(messages=[{"role": "user", "content": code}]).strip()
            print(f"\n[Codevalidator] Validation result:\n{validation}")
            add_message(db, session_id, "codevalidator", validation) 

            if validation.lower().strip() == "no errors found.":
                print("\n✅ Final Output (Code is valid):\n", code)
                break

            # Step 3: Send errors to code generator for fixing
            print("\n[Codevalidator] Errors found, sending back to Codegenerator for fixes.")
            fix_prompt = (
                f"The following errors were found in your code:\n{validation}\n"
                "Please fix these errors and return only the corrected code."
            )
            code = codegenerator.generate_reply(messages=[{"role": "user", "content": fix_prompt}])
            add_message(db, session_id, "codegenerator", code) 
            print(f"\n[Codegenerator] Corrected code:\n{code}")
            iteration += 1

if __name__ == "__main__":
    agentive_code_tool()
