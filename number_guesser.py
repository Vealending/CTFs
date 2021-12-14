from array import *
import requests, time

ENDPOINT = "http://guessing-game:80"
values_to_guess = [[64, 6, 0]]
#values_to_guess = [[64, 6, 0, 8], [128, 11, 1], [2048, 15, 1], [10000, 250, 2]]

def solver():
    for i in range(1):
        n, m, k = values_to_guess[i]
        lies = 0
        
        game_id = start_game(n, m, k)
        print("Game ID:", str(game_id))
        
        full_range = list(range(1, n + 1))
        
        
        for j in range(m):
            print("j:", str(j))
            answer = "A"
            lower_range = full_range[:len(full_range)//2]
            upper_range = full_range[len(full_range)//2:]
            
            print(full_range)
            print(lower_range)
            print(upper_range)
            
            print("Question:", str(lower_range))
            while not isinstance(answer, bool):  
                answer = ask_question(game_id, lower_range)
                print(answer)
            if answer == True:
                full_range = lower_range
            else:
                full_range = upper_range
                
            print("Query:", str(query(game_id)))
            
            if j + 1 == m:
                print(verify_guess(game_id, full_range[0]))
	
def ask_question(game_id, question):
    response = requests.post(f"{ENDPOINT}/ask_question", json={"game_id": game_id, "question": question})
    print("Ask:", str(response.content))
    try:
        return response.json()["answer"]
    except:
        return "Ask fucked game"

def start_game(n, m, k):
    response = requests.post(f"{ENDPOINT}/start_game", json={"N": n, "M": m, "K": k})
    return response.text

def query(game_id):
    response = requests.post(f"{ENDPOINT}/query", json={"game_id": game_id})
    try:
        return response.json()
    except:
        return "Query fucked"

def verify_guess(game_id, guess):
    response = requests.post(f"{ENDPOINT}/verify_guess", json={"game_id": game_id, "guess": guess})
    try:
        return response.json()
    except:
        return "Verify fucked"

if __name__ == '__main__':
    solver()
