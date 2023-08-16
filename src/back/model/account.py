class account:


    def __init__(self, id:int=0, account_name:str='', old_balance:float=0, new_balance:float=0, is_orig:bool=0) -> None:
        self.__id           = id
        self.__account_name = account_name
        self.__old_balance  = old_balance
        self.__new_balance  = new_balance
        self.__is_orig      = is_orig


    def get_id(self) -> int :
        return self.__id

    def set_id(self, id) :
        self.__id = id
        
        
    def get_name(self) -> str :
        return self.__account_name

    def set_name(self, account_name) :
        self.__account_name = account_name
 
 
    def get_old_balance(self) -> float :
        return self.__old_balance

    def set_old_balance(self, old_balance) :
        self.__old_balance = old_balance
        
        
    def get_new_balance(self) -> float :
        return self.__new_balance

    def set_new_balance(self, new_balance) :
        self.__new_balance = new_balance
        
    def get_is_orig(self) -> float :
        return self.__is_orig

    def set_is_orig(self, is_orig) :
        self.__is_orig = is_orig