import AndyBot_MK1 as bot
import AnyBotLog as logg
import DeskBot_MK1
from POM import Desktop_WebPage as wp


def main():
    try:
        deskbot = DeskBot_MK1.DesktopBot()
        deskbot.hashCount_DesktopService()

    except Exception as e:
        logg.logSmth("#" * 20 + "\n")
        logg.logSmth("Exception occurred @#$", 'ERROR')
        logg.logSmth(f"{e}", 'INFO')
        logg.logSmth("#" * 20 + "\n")
    finally:
        logg.logSmth("\n\nEND OF TEST\n")


if __name__ == "__main__": main()
