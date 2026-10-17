"""Actual GTK picker test; temporary data only and no printer calls."""
import configparser,importlib,sys,tempfile,types,json
from pathlib import Path
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GLib,Gdk
sys.path.insert(0,sys.argv[2] if len(sys.argv)>2 else '/home/USER/KlipperScreen')
stage=Path(sys.argv[1]).resolve()
panels=types.ModuleType('panels');panels.__path__=[str(stage)];sys.modules['panels']=panels
class Screen(Gtk.Window):
 def __init__(self):
  super().__init__();c=configparser.ConfigParser();c['main']={}
  self._config=types.SimpleNamespace(get_main_config=lambda:c['main']);self.files=None;self.printer=None
  self.gtk=types.SimpleNamespace(bsidescale=1,Button=lambda *a,**kw:Gtk.Button(label=kw.get('label','')))
 def show_keyboard(self,*a):pass
 def remove_keyboard(self,*a):pass
 def show_panel(self,*a,**kw):raise AssertionError('Unexpected navigation')
 def _confirm_send_action(self,*a,**kw):raise AssertionError('Printer action in isolated test')
def options(combo):return [row[1] for row in combo.get_model()]
with tempfile.TemporaryDirectory() as td:
 store=importlib.import_module('panels.indx_profiles');store.CONFIG=Path(td)
 store.write_json('indx-pa-bases.json',{'PLA base':{'temp':210,'bed':60,'profile':{'enable_pressure_advance':['0'],'pressure_advance':['0']}}})
 profiles=[]
 for ident,brand,material,source,compatible in [('A PLA','Marca A','PLA','system',True),('A PETG','Marca A','PETG','system',True),('B PLA','Marca B','PLA','user',True),('Bad','Esclusa','ABS','system',False)]:
  profiles.append(dict(id=ident,name=ident,brand=brand,material=material,source=source,compatible=compatible,revision='test',config={'nozzle_temperature':['210'],'hot_plate_temp':['60'],'filament_flow_ratio':['1'],'filament_max_volumetric_speed':['12']}))
 store.catalog=lambda:dict(schema=2,profiles=profiles)
 screen=Screen();screen.set_default_size(1024,600)
 panel=importlib.import_module('panels.indx_filaments').Panel(screen,'Filamenti INDX')
 screen.add(panel.content);screen.show_all()
 assert isinstance(panel.brand,Gtk.ComboBoxText) and isinstance(panel.material,Gtk.ComboBoxText)
 assert isinstance(panel.product,Gtk.Label)
 assert panel.scope.get_active()==2
 assert options(panel.brand)==['','Marca A','Marca B'],options(panel.brand)
 assert 'ABS' not in options(panel.material)
 panel.brand.set_active_id('Marca A');panel.material.set_active_id('PETG')
 assert options(panel.profiles)==['A PETG'],options(panel.profiles)
 panel.profiles.set_active_id('A PETG');assert panel.selected['material']=='PETG'
 before={p.name:p.read_bytes() for p in Path(td).iterdir() if p.is_file()}
 def respond(accept,name=''):
  for w in Gtk.Window.list_toplevels():
   if isinstance(w,Gtk.Dialog) and w.get_visible() and w.get_title()=='Nome del filamento':
    if accept:
     for child in w.get_content_area().get_children():
      if isinstance(child,Gtk.Entry):child.set_text(name)
    w.response(Gtk.ResponseType.OK if accept else Gtk.ResponseType.CANCEL);return False
  return True
 GLib.timeout_add(100,respond,False);panel.assign()
 assert before=={p.name:p.read_bytes() for p in Path(td).iterdir() if p.is_file()},'Cancel wrote data'
 GLib.timeout_add(100,respond,True,'Bobina PETG verde');panel.assign()
 r=store.assigned(0);assert r and r['name']=='Bobina PETG verde',panel.status.get_text()
 assert r['brand']=='Marca A' and r['type']=='PETG'
 uid=r['library_id'];panel.activate();assert panel.brand.get_active_id()=='Marca A'
 assert panel.material.get_active_id()=='PETG'
 GLib.timeout_add(100,respond,True,'PETG rinominato');panel.assign()
 assert len(store.library())==1 and store.assigned(0)['library_id']==uid
 panel.scope.set_active(2);panel.brand.set_active_id('Marca B')
 assert panel.material.get_active_id()=='' and options(panel.material)==['','PLA']
 assert not panel.selected
 panel.material.set_active_id('PLA');panel.profiles.set_active_id('B PLA')
 assert panel.selected['brand']=='Marca B'
 panel.scope.set_active(3);assert options(panel.brand)==['','Marca B']
 panel.search.set_text('non presente');assert not panel.selected
 panel.search.set_text('');panel.profiles.set_active_id('B PLA')
 while Gtk.events_pending():Gtk.main_iteration_do(False)
 window=screen.get_window();pix=Gdk.pixbuf_get_from_window(window,0,0,1024,600)
 pix.savev(str(stage/'filament-picker-test.png'),'png',[],[])
 # The name confirmation must also work inside the dashboard proxy.
 dashboard=importlib.import_module('panels.indx_dashboard').Panel(screen,'INDX')
 dashboard.goto('indx_filaments');nested=dashboard.panels['indx_filaments']
 nested.scope.set_active(2);nested.brand.set_active_id('Marca B');nested.material.set_active_id('PLA');nested.profiles.set_active_id('B PLA')
 GLib.timeout_add(100,respond,False);nested.assign()
 assert len(store.library())==1
 dashboard.content.destroy();screen.destroy()
print('PASS actual GTK: dependent brand/material/profile lists, incompatible/source filtering, cancel without writes, name at confirmation, assign/rename stable UUID, dashboard proxy, no printer actions.')
