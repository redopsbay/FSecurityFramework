#!/usr/bin/python3
"""
    Provides Core exception when some sort of condition isn't met.
"""
class FileEmptyError(Exception):
    pass

class ConfigError(Exception):
    pass

class UnHandledSignal(Exception):
    pass

class UnHandledSlot(Exception):
    pass
    
class FileNotSupportedError(Exception):
    pass

class DatabaseConnectionError(Exception):
    pass

class ParameterError(Exception):
    pass
    
class DatabaseConnectionArgumentError(Exception):
    pass

class DictionaryError(Exception):
 	pass