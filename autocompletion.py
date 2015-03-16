from Tkinter import *
import re

lista = [
'Accra',
'Agadir',
'Alicante',
'Amsterdam',
'Ankara',
'Antalya',
'Athenes',
'Atlanta',
'Auckland',
'Baltimore',
'Bangkok',
'Barcelone',
'Bergen',
'Berlin',
'Birmingham',
'Bogota',
'Bologne',
'Boston',
'Brasilia',
'Brisbane',
'Bristol',
'Bruxelles',
'Bucarest',
'Budapest',
'Casablanca',
'Catane',
'Charlotte',
'Cheju',
'Chengdu',
'Chicago',
'Cologne',
'Copenhague',
'Dallas-Fort Worth',
'Delhi',
'Denver',
'Detroit',
'Djeddah',
'Doha',
'Dubai',
'Dublin',
'Durban',
'Dusseldorf',
'Edimbourg',
'Faro',
'Fort Lauderdale',
'Francfort',
'Fukuoka',
'Geneve',
'Glasgow',
'Grande Canarie',
'Guangzhou',
'Hambourg',
'Hangzhou',
'Helsinki',
'Hong-Kong',
'Honolulu',
'Houston',
'Ibiza',
'Istanbul',
'Izmir',
'Jakarta',
'Johannesbourg',
'Kiev',
'Kuala Lumpur',
'Kunming',
'Las Vegas',
'Le Cap',
'Lisbonne',
'Londres',
'Los Angeles',
'Lyon',
'Madrid',
'Malaga',
'Manchester',
'Manille',
'Marrakech',
'Marseille',
'Melbourne',
'Mexico',
'Miami',
'Milan',
'Minneapolis',
'Moscou',
'Mumbai',
'Munich',
'Naples',
'New York',
'Newark',
'Nice',
'Orlando',
'Oslo',
'Palma de Mallorca',
'Paris',
'Philadelphia',
'Phoenix',
'Plaisance',
'Port Elizabeth',
'Porto',
'Prague',
'Pekin',
'Riga',
'Rio De Janeiro',
'Riyadh',
'Rome',
'Saint-Petersbourg',
'Salt Lake City',
'San Diego',
'San Francisco',
'Sao Paulo',
'Sapporo',
'Seattle',
'Seoul',
'Shanghai',
'Shenzhen',
'Singapour',
'Stockholm',
'Stuttgart',
'Sydney',
'Taipei',
'Tampa',
'Tenerife',
'Tokyo',
'Toronto',
'Toulouse',
'Vancouver',
'Varsovie',
'Venise',
'Vienne',
'Washington',
'Xiamen',
'Zurich']

"""newList = lista"""

class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            """words2 = self.comparison2()"""
            if words:            
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    """def setLower(self):
        #global newList
        i = 0
        for element in self.lista:
            i = i + 1
            newList[i] = element.lower()"""

    def comparison(self):
        pattern = re.compile('^' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

    """def comparison2(self):
        print "self" + newList[1]
        pattern = re.compile('^' + self.var.get() + '.*')
        return [w for w in newList if re.match(pattern, w)]"""

"""if __name__ == '__main__':
    root = Tk()

    entry = AutocompleteEntry(lista, root)
    entry.grid(row=0, column=0)
    Button(text='nothing').grid(row=1, column=0)
    Button(text='nothing').grid(row=2, column=0)
    Button(text='nothing').grid(row=3, column=0)

    root.mainloop()"""

def launchDAuto(truc):
    entry = AutocompleteEntry(lista, truc)
    entry.grid(row=3, column=2)
    """entry.setLower()"""
    return entry

def launchAuto(truc):
    entry = AutocompleteEntry(lista, truc)
    entry.grid(row=3, column=3)
    """entry.setLower()"""
    return entry