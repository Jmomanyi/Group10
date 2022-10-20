 
import time as t
def timeofday():
   time=t.strftime("%H")
   if int(time) < 12:
      return "morning"
   elif int(time) >= 12 and int(time) < 17:
      return "afternoon"
   elif int(time) >= 17 and int(time) < 20:
    return "evening"
   else:
     return "night"    
 
tx=timeofday()
print(tx)