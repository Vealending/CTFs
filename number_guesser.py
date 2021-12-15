from array import *
import requests, time, random

ENDPOINT = "http://guessing-game:80"
#values_to_guess = [[64, 6, 0], [128, 11, 1], [2048, 15, 1], [10000, 250, 2]]
values_to_guess = [[128, 11, 1]]

def solver():
    for i in range(50):
        n, m, k = values_to_guess[0]
        no_answer = True
        
        while no_answer:
            asked = 0 
            lies = 0
            
            game_id = start_game(n, m, k)
            full_range = list(range(1, n + 1))
            
            for j in range(m):
                
                lower_range = full_range[:len(full_range)//2]
                upper_range = full_range[len(full_range)//2:]
                answer = "A"
                
                if k != 0: #can lie
                    if not j % 2: # 1, 3, 5
                        #ask once and save
                        question = lower_range
                     
                        answer = ask_question(game_id, question)
                        asked += 1

                        if answer:
                            print("lower")
                            full_range = lower_range
                        else:
                            print("upper")
                            full_range = upper_range

                        temp_full_range = full_range
                        print(temp_full_range)

                    else: # 2, 4, 6 
                        #ask twice and check for lies
                        answer_lower = "A"
                        answer_upper = "A"
                        answer = "A"

                        question = lower_range
                    
                        answer_lower = ask_question(game_id, question)
                        asked += 1

                        question = upper_range
                        answer = "A"

                        answer_upper = ask_question(game_id, question)
                        asked += 1

                        if answer_lower == True and answer_upper == True:
                            print("both true!!")
                            k -= 1
                            question = lower_range
                            answer = ask_question(game_id, question)
                            asked += 1
                            if answer:
                                full_range = lower_range
                            else:
                                full_range = upper_range
                        elif answer_lower == False and answer_upper == False:
                            print("both false!!!")
                            k -= 1
                            question = lower_range
                            answer = ask_question(game_id, question)
                            asked += 1
                            if answer:
                                full_range = lower_range
                            else:
                                full_range = upper_range
                        elif answer_lower == True and answer_upper == False:
                            print("lower mod")
                            full_range = lower_range
                        elif answer_lower == False and answer_upper == True:
                            print("upper mod")
                            full_range = upper_range

                        print("Answers: ", end='')
                        print(answer_lower, answer_upper)

                else: #cannot lie
                
                    question = lower_range
                    
                    answer = ask_question(game_id, question)
                    
                    asked += 1
                    
                    if answer:
                        full_range = lower_range
                    else:
                        full_range = upper_range
                
                print("Status: ", end='')
                print(j, len(full_range), asked, m, k)
                #print("Query:", str(query(game_id)))
                
                if asked == m:
                    print("Successfully exhausted level", str(i))
                    #print("Query:", str(query(game_id)))
                    print(full_range)
                    v = "A"
                    print("Guess:", full_range[0])
                    
                    v = verify_guess(game_id, full_range[0])
                        
                    if v:
                        no_answer = False

                    break
            else:
                continue
            break

	
def ask_question(game_id, question):
    response = requests.post(f"{ENDPOINT}/ask_question", json={"game_id": game_id, "question": question})
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
        print(response.text)
        return response.json()["correct"]
    except:
        return "Verify fucked"

if __name__ == '__main__':
    solver()
