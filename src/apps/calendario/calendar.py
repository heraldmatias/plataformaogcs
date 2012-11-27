# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
import time
import gdata.calendar.data
import gdata.calendar.client
import atom
import random 
from models import Evento
from datetime import datetime
from django.utils.safestring import mark_safe
email = "plataformaintersectorial@gmail.com"
password="cubilfelino!!"
#calendar_client = None
calendar_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
calendar_client.ClientLogin(email, password, calendar_client.source)

color=['%23A32929','%23B1365F','%237A367A','%235229A3','%2329527A','%232952A3','%231B887A',
    '%2328754E','%230D7813','%23528800','%2388880E','%23AB8B00','%23BE6D00','%23B1440E','%23865A5A',
    '%23705770','%234E5D6C','%235A6986','%234A716C','%236E6E41','%238D6F47','%23853104','%23691426',
    '%235C1158','%2323164E','%23182C57','%23060D5E','%23125A12','%232F6213','%232F6309','%235F6B02',
    '%23875509','%238C500B','%23754916','%236B3304','%235B123B','%2342104A','%23113F47','%23333333',
    '%230F4B38','%23856508','%23711616']
def delete_calendar(url_edit):
    if url_edit:
        try:
            calendar_client.Delete(url_edit, None, True)
        except:
            pass
        return True
    return False

def get_or_create(user=None, embed=True,dependencia = None):
    if dependencia:
        calendar_id = _get_or_create_calendar(dependencia.iniciales,embed)
    else:
        calendar_id = _get_or_create_calendar(user.get_dependencia().iniciales,embed)
    if not calendar_id:
        calendar = gdata.calendar.data.CalendarEntry()
        if dependencia:
            calendar.title = atom.data.Title(text=dependencia.iniciales)
            calendar.summary = atom.data.Summary(text=dependencia.__unicode__())
        else:
            calendar.title = atom.data.Title(text=user.get_dependencia().iniciales)
            calendar.summary = atom.data.Summary(text=user.get_dependencia().__unicode__())
        calendar.where.append(gdata.calendar.data.CalendarWhere(value='Lima'))    
        calendar.timezone = gdata.calendar.data.TimeZoneProperty(value='America/Los_Angeles')
        calendar.hidden = gdata.calendar.data.HiddenProperty(value='false')
        calendar.color = gdata.calendar.data.ColorProperty(value='#2952A3')#RGBToHTMLColor())
        new_calendar = calendar_client.InsertCalendar(new_calendar=calendar)      
        rule = gdata.calendar.data.CalendarAclEntry()
        rule.scope = gdata.acl.data.AclScope(type="default")
        roleValue = 'http://schemas.google.com/gCal/2005#%s' % ('read')
        rule.role = gdata.acl.data.AclRole(value=roleValue)
        aclUrl = new_calendar.get_acl_link().href 
        returned_rule = calendar_client.InsertAclEntry(rule, aclUrl)        
        calendar_id = (embed and new_calendar.content.src.split('/')[5].replace('%40','@')
            or a_calendar.content.src )
    return calendar_id

def _get_or_create_calendar(calendar_name, embed=True):
    print calendar_name
    feed = calendar_client.GetOwnCalendarsFeed()#GetAllCalendarsFeed()
    calendar_id = None
    for a_calendar in feed.entry:        
        if a_calendar.title.text == calendar_name:
            calendar_id = (embed and a_calendar.content.src.split('/')[5].replace('%40','@')
            or a_calendar.content.src)
            break
    return calendar_id

def insert_or_update_event(evento, url_edit=None):
    calendar = get_or_create(evento.idusuario_creac,False)    
    if url_edit:
        calendar_client.Delete(url_edit, None, True) #borrar de google calendar        
    event = gdata.calendar.data.CalendarEventEntry()
    event.title = atom.data.Title(text=u'%s: %s' %
        (evento.idusuario_creac.get_dependencia().iniciales, evento.titulo))
    event.content = atom.data.Content(text=evento.descripcion)
    event.where.append(gdata.calendar.data.CalendarWhere(value=evento.lugar))
    event.color = gdata.calendar.data.ColorProperty(value='#000000')
    
    start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',
        time.gmtime(time.mktime(datetime.combine(evento.fec_inicio, evento.hor_inicio).timetuple())))
    end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',
        time.gmtime(time.mktime(datetime.combine(evento.fec_termin, evento.hor_termin).timetuple())))
    #end_time = datetime.combine(f, h).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    #start_time2 = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
    
    #end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 3600))
    event.when.append(gdata.calendar.data.When(start=start_time, end=end_time))

    new_event = calendar_client.InsertEvent(event,calendar)
    evento.url_edit = new_event.GetEditLink().href    
    evento.save()
    return True#new_event

def events(calendar):
  feed = calendar_client.GetCalendarEventFeed(uri=calendar)
  print 'Events on Primary Calendar: %s' % (feed.title.text,)
  for i, an_event in enumerate(feed.entry):
    print '\t%s. %s' % (i, an_event.title.text,)
    #for p, a_participant in enumerate(an_event.who):
    #  print '\t\t%s. %s' % (p, a_participant.email,)
    #  print '\t\t\t%s' % (a_participant.attendee_status.value,)

def RGBToHTMLColor():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    rgb_tuple = (r,g,b)
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor

def _InsertEvent(cal_client, title='Tennis with Beth',
      content='Meet for a quick lesson', where='On the courts',
      start_time=None, end_time=None, recurrence_data=None):
    """Inserts a basic event using either start_time/end_time definitions
    or gd:recurrence RFC2445 icalendar syntax.  Specifying both types of
    dates is not valid.  Note how some members of the CalendarEventEntry
    class use arrays and others do not.  Members which are allowed to occur
    more than once in the calendar or GData "kinds" specifications are stored
    as arrays.  Even for these elements, Google Calendar may limit the number
    stored to 1.  The general motto to use when working with the Calendar data
    API is that functionality not available through the GUI will not be
    available through the API.  Please see the GData Event "kind" document:
    http://code.google.com/apis/gdata/elements.html#gdEventKind
    for more information"""
    #recurrence_data = ('DTSTART;TZID=America/Lima:' + start_time +'\r\n'
    #                   + 'DTEND;TZID=America/Lima:' + end_time + '\r\n'
    #                   + 'RRULE:FREQ=DAILY;UNTIL='+end_time2+'\r\n'
    #                   + 'BEGIN:VTIMEZONE\r\n'
    #                   + 'TZID:America/Lima\r\n'
    #                   + 'X-LIC-LOCATION:America/Lima\r\n'
    #                   + 'END:VTIMEZONE\r\n'
    #                   )
    event = gdata.calendar.data.CalendarEventEntry()
    event.title = atom.data.Title(text=title)
    event.content = atom.data.Content(text=content)
    event.where.append(gdata.data.Where(value=where))
    event.color = gdata.calendar.data.ColorProperty(value='#000000')

    if recurrence_data is not None:
        event.recurrence = gdata.data.Recurrence(text=recurrence_data)
    else:
        if start_time is None:
        # Use current time for the start_time and have the event last 1 hour
            start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
            end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',
                                     time.gmtime(time.time() + 3600))
        event.when.append(gdata.data.When(start=start_time,
                                          end=end_time))    
    new_event = cal_client.InsertEvent(event)
    return new_event

def getinframe(calendar_name = None):
    feed = calendar_client.GetOwnCalendarsFeed()
    begin="""<iframe src="https://www.google.com/calendar/embed?showTitle=0&amp;ctz=America%2FLima&amp;
    showPrint=0&amp;showTabs=0&amp;showTz=0&amp;height=400&amp;wkst=1&amp;bgcolor=%23ffffff&amp;"""
    end='style=" border-width:0 " width="690" height="400" frameborder="0" scrolling="no"></iframe>';
    result=''
    result+=begin
    i=0
    l=len(color)
    if calendar_name:
        result+='src='+get_or_create(dependencia=calendar_name)+"&amp;color="+color[i]+'&amp;'+end
    else:        
        for co, entry in enumerate(feed.entry):
            if co == 0:
                continue
            entry=entry.content.src.split('/')[5].replace('%40','@')
            result+='src='+entry+"&amp;color="+color[i]+'&amp;'
            if i<l:
                i=i+1
            else:
                i=0
        result+=end    
    return mark_safe(result)
