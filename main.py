from src.agent import ask_agent

def main():
    print("Custom Agent running. Type 'exit' to quit.\n")
    while True:
        q = input("Ask your agent: ")
        if q.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        try:
            answer = ask_agent(q)
            print("Agent:", answer, "\n")
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()
