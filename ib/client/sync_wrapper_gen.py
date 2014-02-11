__author__ = 'oglebrandon'
import inspect
from ib.ext.EWrapper import EWrapper

class_fields = []
refs = EWrapper
for func in dir(refs):
    if func[0] != '_':
        if inspect.ismethod(eval('refs.' + str(func))):
            [class_fields.append(x) for x in inspect.getargspec(eval(
                'refs.' + str(func))).__dict__['args'][1:]]
print ' \n'.join([x + ' = None' for x in list(set(class_fields))])

funcs = {}
for func in dir(refs):
    if func[0] != '_':
        if inspect.ismethod(eval('refs.' + str(func))):
            local = inspect.getargspec(eval('refs.' + str(func))).__dict__['args'][1:]

            args= ', '.join(local)
            caller = 'self.handler = sys._getframe().f_code.co_name'
            fields = "if '"  + str(func) + "' in self.emitter: \n\t\tmsg = "\
                     + "{" +'\n\t\t\t\t'.join(["'" + str(var) +"' : " +str(var) + ',' for var in local])[:-1] + '}' \
                     + '\n\t\tif msg not in self.return_list:\n\t\t\tself.return_list.append(msg)'\
                     + '\n\tif self.return_list:\n\t\t' + str(caller)\
                     + "\n\tif self.suppress is False:\n"\
                     +   "\t\tshowmessage('{func}', vars())".format(func=func)

            method =("""def {func}(self{params}):{fields}
            """).format(func=func,
                        params= ', ' + args if args is not '' else args,
                        fields= '\n\t'  + fields)

            print method



