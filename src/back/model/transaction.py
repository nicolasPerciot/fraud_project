class transaction:


    def __init__(self, id:int=0, step:int='', trans_type:str='', amount:float='', is_fraud:bool=0) -> None:
        self.__id               = id
        self.__step             = step
        self.__trans_type       = trans_type
        self.__amount           = amount
        self.__is_fraud         = is_fraud


    def get_id(self) -> int :
        return self.__id

    def set_id(self, id) :
        self.__id = id
        
        
    def get_step(self) -> int :
        return self.__step

    def set_step(self, step) :
        self.__step = step


    def get_trans_type(self) -> str :
        return self.__trans_type

    def set_trans_type(self, trans_type) :
        self.__trans_type = trans_type
        
        
    def get_amount(self) -> float :
        return self.__amount

    def set_amount(self, amount) :
        self.__amount = amount
        
        
    def get_is_fraud(self) -> bool :
        return self.__is_fraud

    def set_is_fraud(self, is_fraud) :
        self.__is_fraud = is_fraud