from collections import defaultdict

class Parser:

    def __init__(self, grammar:defaultdict , entry_symbol:chr):
        self.grammar = grammar
        self.entry_symbol = entry_symbol
        self.first = defaultdict(set)
        self.follow  = defaultdict(set)
        self.parsing_table = defaultdict()
        self.get_first()
        self.get_follow()
        self.get_parsing_table()
    
    def isNonTerminal(self, symbol:str) -> bool:
        if symbol in self.grammar.keys():
            return True
        return False
    
    def first_util(self, produc:str) -> list:
        for deriv in self.grammar[produc]:
            symbol = deriv[0]
            if not self.isNonTerminal(symbol):
                self.first[produc].add(symbol)
            else:
                self.first[produc] = self.first[produc].union(self.first_util(symbol))
        return self.first[produc]
    
    def get_first(self) -> defaultdict:
        for produc in self.grammar.keys():
            self.first[produc]
        for produc,deriv in self.grammar.items():
            self.first_util(produc)
        return self.first

    def printFirst(self) -> None:
        print("First Set: ")
        for key, val in self.first.items():
            print(f"{key} : {val}")
    
    def follow_util(self, non_term:chr) -> list[list:chr]:
        for new_non_term, deriv in self.grammar.items():
            for sub_deriv in deriv:
                for i in range(len(sub_deriv)):
                    if sub_deriv[i] == non_term:
                        if i+1 < len(sub_deriv):
                            beta = sub_deriv[i+1]
                            if self.isNonTerminal(beta):
                                self.follow[non_term] = self.follow[non_term].union(self.first[beta])
                                self.follow[non_term].discard('eps')
                            else:
                                self.follow[non_term].add(beta)
                            if 'eps' in self.first[beta] and new_non_term != beta:
                                self.follow[non_term] = self.follow[non_term].union(self.follow_util(new_non_term))
                        elif i+1 == len(sub_deriv) and new_non_term != non_term:
                            if self.isNonTerminal(sub_deriv[i]):
                                self.follow[non_term] = self.follow[non_term].union(self.follow_util(new_non_term))
        return self.follow[non_term]

                        
    def get_follow(self) -> defaultdict:
        for non_term in self.grammar.keys():
            if non_term == self.entry_symbol:
                self.follow[non_term].add('$')
            else:
                self.follow[non_term]
        for non_term in self.grammar.keys():
            self.follow_util(non_term)
        return self.follow

    def printFollow(self) -> None:
        print("Follow Set: ")
        for key, val in self.follow.items():
            print(f"{key} : {val}")
    
    """def get_parsing_table(self):
        for non_term, deriv in self.grammar.items():
            for sub_deriv in deriv:
                symbol = sub_deriv[0]
                if self.isNonTerminal(symbol):
                    for terminal in self.first[symbol]-{'eps'}:
                        self.parsing_table[non_term, terminal] = {non_term:sub_deriv}
                elif symbol == "eps" or symbol in self.first[symbol]:
                    for terminal in self.follow[non_term]:
                        self.parsing_table[non_term, terminal] = {non_term:['eps']}
                else:
                    self.parsing_table[non_term,symbol] = {non_term, sub_deriv}
        print(self.parsing_table)
        return self.parsing_table"""

    def get_parsing_table(self):
        for key,rule in self.grammar.items():
            for sub_rule in rule:
                symbol = sub_rule[0]
                if self.isNonTerminal(symbol): 
                    for ter in self.first[symbol]-{'eps'}:
                        self.parsing_table[key,ter]={key:sub_rule}
                       

                elif symbol=="eps" or symbol in self.first[symbol]:
                    for ter in self.follow[key]:
                        self.parsing_table[key,ter] = {key:['eps']}
                
                else:
                    self.parsing_table[key,symbol]={key:sub_rule}
                    
        #print(self.parsing_table)  #for printing terminals, non_terminals and their entries in Parsing_table
        #return parsing_table
    
    def printTable(self) -> None:
        print("Parsing Table: ")
        for key, val in self.parsing_table.items():
            print(f"{key} : {val}")


    

if __name__ == "__main__":
    start_state='E'
    dic={   
        "E" : [ ["T","E1"] ],
        "T" : [ ["F","T1"] ],
        "F" : [ ["id"], ["(","E",")"] ],
        "E1": [ ["+","T","E1"], ["-","T","E1"], ["eps"] ],
        "T1": [ ["*","F","T1"], ["/","F","T1"], ["eps"], ["^","F","T1"] ]
    }
    parser = Parser(dic, start_state)
    parser.printFirst()
    parser.printFollow()
    parser.printTable()





    