"""Isolated real GTK layout/navigation tests. Never connects to the printer."""
import configparser,importlib,sys,tempfile,types,json
from pathlib import Path
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GLib,Gdk
ks=Path(sys.argv[2]) if len(sys.argv)>2 else Path('/home/sovol/KlipperScreen')
sys.path.insert(0,str(ks))
stage=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/home/sovol/indx-preview-0.2.0')
panels=types.ModuleType('panels');panels.__path__=[str(stage)];sys.modules['panels']=panels
class Screen(Gtk.OffscreenWindow):
 def __init__(self):
  super().__init__();c=configparser.ConfigParser();c['main']={}
  self._config=types.SimpleNamespace(get_main_config=lambda:c['main']);self.files=None;self.printer=None
  self.gtk=types.SimpleNamespace(bsidescale=1,Button=lambda *a,**kw:Gtk.Button(label=kw.get('label','')))
 def show_keyboard(self,*a):pass
 def remove_keyboard(self,*a):pass
 def show_panel(self,*a,**kw):raise AssertionError('Unexpected navigation')
 def _confirm_send_action(self,*a,**kw):raise AssertionError('Printer action in isolated test')
css=Gtk.CssProvider();base=(ks/'styles/base.css').read_text().replace('KS_FONT_SIZE','20');css.load_from_data((base+(stage/'indx-ui.css').read_text()).encode());Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
with tempfile.TemporaryDirectory() as td:
 store=importlib.import_module('panels.indx_profiles');store.CONFIG=Path(td)
 store.write_json('indx-pa-bases.json',{'PLA base':{'temp':210,'bed':60,'profile':{'enable_pressure_advance':['0'],'pressure_advance':['0']}}})
 importlib.import_module('panels.indx_pa').CONFIG=Path(td)
 machine=importlib.import_module('panels.indx_machine_panel');machine.Panel.reload=lambda self,*a:None
 for count in (1,4,8,12):
  store.confirm_hardware([dict(tool=t,diameter=[.4,.4,.6,.8][t%4],type='standard',cht_multiplier=1.3) for t in range(count)])
  for width,height in ((1024,600),(1280,720)):
   screen=Screen();screen.set_size_request(width,height);screen.resize(width,height)
   module=importlib.import_module('panels.indx_dashboard');dash=module.Panel(screen,'INDX Studio');screen.add(dash.content);screen.show_all()
   for _,name in module.PAGES:
    dash.goto(name)
    if name=='indx_machine_panel':
     p=dash.panels[name];p.data=dict(schema=1,dock_dir=-1,clearance_y=80,trigger_offset=5,z_hop=3,tools=[dict(tool=t,diameter=.4,type='standard',cht_multiplier=1.3,x=30+t*35,dock_y=30,offset_x=0,offset_y=0,offset_z=0) for t in range(count)]);p.display();assert len(p.gather()['tools'])==count
    while Gtk.events_pending():Gtk.main_iteration_do(False)
    assert dash.visible_name==name
    assert screen.get_size().width<=width,(count,width,name,screen.get_size())
    assert screen.get_size().height<=height,(count,height,name,screen.get_size())
    if count==4 and width==1280 and name in ('overview','indx_filaments','indx_machine_panel','indx_pa'):
     screen.get_pixbuf().savev(str(stage/('studio-'+name+'.png')),'png',[],[])
   dash.goto('indx_max_flow',count-1);assert dash.panels['indx_max_flow'].tool.get_active()==count-1
   dash.goto('overview');assert len(dash.overview.get_children()[1].get_children())==count
   screen.destroy()
  print('PASS studio navigation/layout:',count,'tools, 1024x600 and 1280x720')
print('PASS CSS parse, 8 pages, selected tool propagation, variable tool overview, no printer calls.')
