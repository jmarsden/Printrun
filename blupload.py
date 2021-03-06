#!/usr/bin/env python
#
# Copyright 2011 Kliment Yanev <kliment.yanev@gmail.com>
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
import printcore,time,sys,os

def dosify(name):
    return os.path.split(name)[1].split(".")[0][:8]+".g"

def blupload(printer,filename,path):
    printer.send_now("M28 "+dosify(filename))
    printer.startprint([i.replace("\n","") for i in open(path)])
    try:
        sys.stdout.write("Progress: 00.0%")
        sys.stdout.flush()
        while(printer.printing):
            time.sleep(1)
            sys.stdout.write("\b\b\b\b%02.1f%%" % (100*float(printer.queueindex)/len(printer.mainqueue),) )
            sys.stdout.flush()
        printer.send_now("M29 "+dosify(filename))
        print "Done uploading, disconnecting with a 5 second timeout in case the printer has something important to say."
        printer.disconnect()
        time.sleep(5)
        print "Upload complete. Goodbye!" 
        
    except:
        print "Abort, disconnecting with a 5 second timeout in case the printer has something important to say."
        printer.disconnect()

if __name__ == '__main__':
    #print "Usage: python blupload.py filename.gcode"
    filename="../prusamendel/sellsx_export.gcode"
    tfilename=filename
    if len(sys.argv)>1:
        filename=sys.argv[1]
        tfilename=os.path.basename(sys.argv[1])
        print "Uploading: "+filename," as "+dosify(tfilename)
        p=printcore.printcore('/dev/ttyUSB0',115200)
        p.loud=False
        time.sleep(2)
        blupload(p,tfilename,filename)
        
    else:
        print "Usage: python blupload.py filename.gcode"

