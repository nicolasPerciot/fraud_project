class user:
      
        
    def __init__(self, id:int=0, username:str='', password:str=''):
        self.__id       = id
        self.__username = username
        self.__password = password

    
    def get_id(self) -> str :
        return self.__id

    def set_id(self, id) :
        self.__id = id
        
        
    def get_username(self) -> str :
        return self.__username

    def set_username(self, username) :
        self.__username = username


    def get_password(self) -> str :
        return self.__password

    def set_password(self, password) :
        self.__password = password