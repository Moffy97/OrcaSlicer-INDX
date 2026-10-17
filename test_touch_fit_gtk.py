"""Isolated real GTK layout/navigation tests. Never connects to the printer."""
import configparser,importlib,sys,tempfile,types,json
from pathlib import Path
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GLib,Gdk
sys.path.insert(0,sys.argv[2])
stage=Path(sys.argv[1])
panels=types.ModuleType('panels');panels.__path__=[str(stage)];sys.modules['panels']=panels
class Screen(Gtk.OffscreenWindow):
 def __init__(self,width,height):
  super().__init__();c=configparser.ConfigParser();c['main']={}
  self._config=types.SimpleNamespace(get_main_config=lambda:c['main']);self.files=None;self.printer=None
  self.width=width;self.height=height;self.vertical_mode=False;self.theme='material-dark'
  from ks_includes.KlippyGtk import KlippyGtk
  self.gtk=KlippyGtk(self)
 def reset_screensaver_timeout(self,*a):pass
 def show_keyboard(self,*a):pass
 def remove_keyboard(self,*a):pass
 def show_panel(self,*a,**kw):raise AssertionError('Unexpected navigation')
 def _confirm_send_action(self,*a,**kw):raise AssertionError('Printer action in isolated test')
css=Gtk.CssProvider();base=(Path(sys.argv[2])/'styles/base.css').read_text().replace('KS_FONT_SIZE','32');css.load_from_data((base+(stage/'indx-ui.css').read_text()).encode());Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
with tempfile.TemporaryDirectory() as td:
 store=importlib.import_module('panels.indx_profiles');store.CONFIG=Path(td)
 store.write_json('indx-pa-bases.json',{'PLA base':{'temp':210,'bed':60,'profile':{'enable_pressure_advance':['0'],'pressure_advance':['0']}}})
 importlib.import_module('panels.indx_pa').CONFIG=Path(td)
 machine=importlib.import_module('panels.indx_machine_panel');machine.Panel.reload=lambda self,*a:None
 for count in (4,12):
  store.confirm_hardware([dict(tool=t,diameter=[.4,.4,.6,.8][t%4],type='standard',cht_multiplier=1.3) for t in range(count)])
  for width,height in ((1024,600),(1280,800)):
   if count==4 and width==1280:
    profile=dict(id='Demo PLA',name='Demo PLA',brand='Generic',material='PLA',compatible=True,config={'nozzle_temperature':['210'],'hot_plate_temp':['60'],'filament_flow_ratio':['.98'],'filament_max_volumetric_speed':['12']})
    import zlib
    (store.CONFIG/'indx-orca-catalog-cache.json.z').write_bytes(zlib.compress(json.dumps(dict(schema=2,profiles=[profile])).encode()))
    for t in range(count):store.assign_profile(store.stock_record(profile,t,'#22AA66'),t)
   if count==4 and width==1280:
    profile=dict(id='Demo PLA',name='Demo PLA',brand='Generic',material='PLA',compatible=True,config={'nozzle_temperature':['210'],'hot_plate_temp':['60'],'filament_flow_ratio':['.98'],'filament_max_volumetric_speed':['12']})
    import zlib
    (store.CONFIG/'indx-orca-catalog-cache.json.z').write_bytes(zlib.compress(json.dumps(dict(schema=2,profiles=[profile])).encode()))
    for t in range(count):store.assign_profile(store.stock_record(profile,t,'#22AA66'),t)
   screen=Screen(width,height);screen.set_size_request(width,height);screen.resize(width,height)
   module=importlib.import_module('panels.indx_dashboard');dash=module.Panel(screen,'INDX Studio')
   frame=Gtk.Grid();bar=Gtk.Box();bar.set_size_request(int(width*.1),height);title=Gtk.Label(label='KlipperScreen · Cornice nativa');title.set_size_request(-1,int(screen.gtk.titlebar_height));frame.attach(bar,0,0,1,2);frame.attach(title,1,0,1,1);frame.attach(dash.content,1,1,1,1);screen.add(frame);screen.show_all()
   for _,name in module.PAGES:
    dash.goto(name)
    if name=='indx_machine_panel':
     p=dash.panels[name];p.data=dict(schema=1,dock_dir=-1,clearance_y=80,trigger_offset=5,z_hop=3,tools=[dict(tool=t,diameter=.4,type='standard',cht_multiplier=1.3,x=30+t*35,dock_y=30,offset_x=0,offset_y=0,offset_z=0) for t in range(count)]);p.display();assert len(p.gather()['tools'])==count
    while Gtk.events_pending():Gtk.main_iteration_do(False)
    assert dash.visible_name==name
    assert screen.get_size().width<=width,(count,width,name,screen.get_size())
    assert screen.get_size().height<=height,(count,height,name,screen.get_size())
    # The full workspace viewport and its footer must remain within the
    # available native frame, not merely within an isolated test window.
    pos=dash.viewport.translate_coordinates(screen,0,0);a=dash.viewport.get_allocation();assert pos[1]+a.height<=height,(name,'viewport clipped',pos,a.height)
    if name=='indx_filaments':
     footer=dash.panels[name].content.get_children()[-1];pos=footer.translate_coordinates(screen,0,0);a=footer.get_allocation();assert pos[1]+a.height<=height,(name,'confirm clipped',pos,a.height)
    if count==4 and width==1280 and name=='overview':
     def labels(widget):
      return [widget.get_text()] if isinstance(widget,Gtk.Label) else [text for child in widget.get_children() for text in labels(child)] if isinstance(widget,Gtk.Container) else []
     text='\n'.join(labels(dash.overview));assert 'FLOW 0.98' in text and 'PORTATA 12' in text and 'PA 0' in text and 'standard / stimato' in text,text
    if count==4 and width==1280 and name in ('overview','indx_filaments','indx_machine_panel','indx_pa'):
     screen.get_pixbuf().savev(str(stage/('touch-fit-'+name+'.png')),'png',[],[])
   dash.goto('indx_max_flow',count-1);assert dash.panels['indx_max_flow'].tool.get_active()==count-1
   dash.goto('overview');assert len(dash.overview.get_children()[1].get_children())==count
   screen.destroy()
  print('PASS real KlippyGtk buttons, 32px system font, native frame:',count,'tools, 1024x600 and 1280x800')
print('PASS CSS parse, 8 pages, selected tool propagation, variable tool overview, no printer calls.')
