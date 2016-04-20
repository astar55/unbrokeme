from django import template
from datetime import date
import calendar

register = template.Library()

@register.simple_tag
def getbudmonth():
    today = date.today()
    currentmonth = today.month
    currentyear = today.year
    numdays = calendar.monthrange(currentyear, currentmonth)
    return ("%d/01/%d - %d/%02d/%d" % ((currentmonth), (currentyear)\
    , (currentmonth), (numdays[1]), (currentyear)))
     
@register.simple_tag
def getcurrentdate():
    today = date.today()
    return ("%d-%02d-%d" % ((today.year), (today.month), (today.day)))