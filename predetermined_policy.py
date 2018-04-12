
		
def predetermined_policy(cls):
    """
    Function returns a policy dictionary where the policy is predetermined according to
    the following strategy: (1) if high card is >=Jack or have a pair, then bet if possible and 
    otherwise call, (2) if high card is 10 or 9, then check if possible and otherwise call, and
    (3) in all other cases, check if possible and otherwise fold
    """
    policy_dict = dict()
    
    for is_same_suit in range(2):
        
        for high_card in range(13):
            for low_card in range(high_card + 1):
                for state_idx in range(len(STATES)):
                    
                    # At first set all elements of policy_dict to zero
                    for action in ACTIONS[state_idx]:
                        
                        full_state = (is_same_suit, high_card, low_card, STATES[state_idx], action)
                        policy_dict[full_state] = 0
                    
                    
                    # Aggressive policy when high card is >= J or have a pair
                    # Bet if possible, otherwise call
                    if (high_card>=9 or high_card==low_card):
                        if 'B' in ACTIONS[state_idx]:
                            full_state = (is_same_suit, high_card, low_card, STATES[state_idx], 'B')
                            policy_dict[full_state] = 1
                        else:
                            full_state = (is_same_suit, high_card, low_card, STATES[state_idx], 'C')
                            policy_dict[full_state] = 1

                        

                    # Safe policy when high card is 10 or 9
                    # Check if possible, otherwise call
                    elif (high_card==7 or high_card==8):
                        if 'Ch' in ACTIONS[state_idx]:
                            full_state = (is_same_suit, high_card, low_card, STATES[state_idx], 'Ch')
                            policy_dict[full_state] = 1
                        else:
                            full_state = (is_same_suit, high_card, low_card, STATES[state_idx], 'C')
                            policy_dict[full_state] = 1
                        
                    
                    # Passive policy otherwise
                    else:
                        if 'Ch' in ACTIONS[state_idx]:
                            full_state = (is_same_suit, high_card, low_card, STATES[state_idx], 'Ch')
                            policy_dict[full_state] = 1
                        else:
                            full_state = (is_same_suit, high_card, low_card, STATES[state_idx], 'F')
                            policy_dict[full_state] = 1
    return cls(policy_dict)

#%%
