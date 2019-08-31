def SunRiseAndSet( lat,lon,tz,elev ):

    from astral import Location
    l = Location(('', '', lat, lon, tz, elev))
    sun = l.sun()
    return sun


latitude = eval( input("纬度：") )
longitude = eval( input("经度：") )
elevation = 0
timezone = 'Asia/Shanghai'

sun = SunRiseAndSet( latitude, longitude, timezone, elevation )

print()
print("日出: ", str(sun['sunrise']))
print("日落: ", str(sun['sunset']))

