import chess
import subprocess
import json

def ollama_suggest_move(board):
    # Prepare the prompt for Ollama
    prompt = f"The current chess board is:\n{board}\nSuggest the best move for white."
    
    # Run the Ollama CLI (or API if available)
    result = subprocess.run(
        ["ollama", "run", "llama3.1"],
        input=prompt,
        text=True,
        capture_output=True
    )
    
    if result.returncode != 0:
        raise Exception(f"Ollama failed: {result.stderr}")
    
    # Parse and return the move from the output
    output = result.stdout
    # You might need to process or extract the move from Ollama's response format
    return output.strip()

def main():
    board = chess.Board()
    while not board.is_game_over():
        print(board)
        user_move = input("Your move (in algebraic notation, e.g., e2e4): ")

        if chess.Move.from_uci(user_move) in board.legal_moves:
            board.push_uci(user_move)
        else:
            print("Illegal move. Try again.")
            continue

        print("\nOllama's Turn:")
        try:
            ollama_move = ollama_suggest_move(board)
            print(f"Ollama suggests: {ollama_move}")
            # If you want to apply the move directly:
            move = chess.Move.from_uci(ollama_move)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Ollama suggested an illegal move!")
        except Exception as e:
            print(f"Error: {e}")
            break

    print("Game Over!")
    print(board.result())

if __name__ == "__main__":
    main()