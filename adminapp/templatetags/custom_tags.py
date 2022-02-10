from django import template

register = template.Library()

@register.filter(name='split')
def split(str, key):
    return str.split(key)

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def getRecord(queryset,num):
    print(num)
    return queryset[num-1]


@register.filter
def countProjectCarousel(x,args): #HomePage Project carousel  
    num =  ((x-1)*5) + args
    return num

@register.filter(name='compareString')
def compareString(str1,str2): #compare string 
       return str1==str2

