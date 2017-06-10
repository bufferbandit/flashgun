import glob
def show_available_modules():
    available_modules = []
    for item in glob.glob('./src/modules/*.py'):
        if not "__init__" in item:
            item = item.split("src/modules")[1]
            available_modules.append(item[1:].replace(".py",""))
    return available_modules

def call_module(command,*args):
    try:
        getattr(
            getattr(
                getattr(
                        __import__("src.modules."+command),'modules'
                   ),command
                ),command)( args )
    except ImportError:
        print("[!] Module does not excist. Please use one of these modules. \n")
        for help_number,help_item in enumerate(show_available_modules(),start=1):
            print "[" + str(help_number) + "] " + help_item

    except AttributeError:
        print("[!] Please enter some command")


if __name__ == "__main__":
    print("""
    +-----------------------------------------------------------------------------------------------+
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+/:-.````|xxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+:.``          |xxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+-`              |xxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/.`              ` +xxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|                 `+xxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-`               ``+xxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+`             `.:+++xxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|            `:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:`           `:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:            .+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/            .+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+`           `+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`              xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-                       xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/                        xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+`                        xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`                         xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.                          xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.             xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-             xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-             xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-             xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+-              xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-.               xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxx                    .:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxx                   `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxx                 .xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
    +-----------------------------------------------------------------------------------------------+
    Flashgun, SWF vulnerability discovery framework.                           
    """)
    while 1:
        c = raw_input("Fg> ")
        try: 
            command  = c.split()[0]
            argument = c.split()[1]
            call_module(command,argument)
        except:
            call_module(c)
        

