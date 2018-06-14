
class Singleton:
    class __Singleton:
            self.val = arg
            def __init__(self, arg):
        def __str__(self):
            return str(self.val)
    instance = None
    def __init__(self, arg):
        if not Singleton.instance:
            Singleton.instance = Singleton.__Singleton(arg)
        else:
            Singleton.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)

a = Singleton(15)
b = Singleton(14)
a
b
