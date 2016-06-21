#fname = self._check_for_save_dir(suggestedfile, self.wildcardsCSV)
import Tkinter
def whichFile(wildcards, suggestedfile, directory):
    root = Tkinter.Tk()
    try:
        if suggestedfile !="":
            fname = tkFileDialog.asksaveasfilename(initialfile = suggestedfile, initialdir = directory, filetypes=(wildcards))
        else:
            fname = tkFileDialog.asksaveasfilename(filetypes=(wildcards))
    except:
        print "Directory string empty. Please load a file first"
        fname =""
    root.destroy()
    return fname