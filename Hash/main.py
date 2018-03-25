import sys,os,math,random,pdb

from hashtable import HASH


#-------------------------------------------------------------
def HashF_str(key,M) :
#-------------------------------------------------------------
   r = 0
   for c in key : r = r*256 + ord(c)
   return( r%M )

#-------------------------------------------------------------
# main
#-------------------------------------------------------------
M = int(input("M? "))
print("\nLoading \"Project1.txt\"...")

IN = open("hash_key.txt",'r')
h = HASH(M,HashF_str)
itemdata = 0
for itemkey in IN :
   key = itemkey.rstrip('\n')
   itemdata += 1
   if ( key in h ):
      print("({},{:3d}) duplicate key. Ignored.".format(key,itemdata))
   else :
      if   ( itemdata%4 == 0 ) : h.Add(key,itemdata)
      elif ( itemdata%4 == 1 ) : h = h + (key,itemdata)
      elif ( itemdata%4 == 2 ) : h = (key,itemdata) + h
      else :                     h += (key,itemdata)
IN.close()
try :
   assert ( h.M <= len(h) )
except AssertionError :
   print("\nYour choice of M is too big! Try again")
print("\nBefore deletions...")
print ('N = \t%d, M = \t%d'%(h.N,h.M))
print(str(h))
DELETIONS = 4

print("Making {:3d} deletions...".format(DELETIONS))
random.seed()
for i in range (0,DELETIONS) :
   deleted = False
   count = 0
   while ( not deleted ) :
      itemkey = ""
      for i in range(1,3+1) :
         itemkey += chr(random.randint(0,25)+ord('A'))
      count += 1
      try :
         print("({},{:3d}) found after {:6d} tries. Deleted.".format(itemkey,h[itemkey],count))
         if   ( h[itemkey]%4 == 0 ) : h.Sub(itemkey)
         elif ( h[itemkey]%4 == 1 ) : h = h - itemkey
         elif ( h[itemkey]%4 == 2 ) : h = itemkey - h
         else :                       h.Sub(itemkey)
         deleted = True
      except KeyError :
         pass

print("\nAfter {:3d} deletions...".format(DELETIONS))
print ('N = \t%d, M = \t%d'%(h.N,h.M))
print(str(h))

del h

sys.exit( 0 )